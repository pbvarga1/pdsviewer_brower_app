import logging
import threading
from io import BytesIO

from redis import Redis
from flask import Flask, make_response, request, render_template, jsonify

import requests
from planetaryimage import decoders
from matplotlib.figure import Figure
from planetaryimage import PDS3Image as _PDS3Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

logger = logging.getLogger(__name__)

# Use these constants if you are building the docker image
HOST = '0.0.0.0'
PORT = 80
REDIS_HOST = 'redis'

# Use these constants if you are running on local host
# HOST = '127.0.0.1'
# PORT = 5000
# REDIS_HOST = None


class BandSequentialDecoder(decoders.BandSequentialDecoder):

    @property
    def size(self):
        return int(super(BandSequentialDecoder, self).size)


class PDS3Image(_PDS3Image):
    """Extend the PDS3Image class to open images by URL"""

    @staticmethod
    def _get_name_from_url(url):
        name = url.split('/')[-1]
        return name

    @classmethod
    def _get_content(cls, url, rcache=None):
        name = cls._get_name_from_url(url)
        if isinstance(rcache, Redis) and rcache.hexists('image', name):
            content = rcache.hget('image', name)
        else:
            with requests.get(url, stream=True) as r:
                content = r.content
                rcache.hset('image', name, content)
        return content

    @classmethod
    def open_url(cls, url, rcache=None):
        """Open an image from the url to the image in the PDS

        Paramters
        ---------
        url : str
            Url of image. If the image is detached, use the label
        rache : Redis [None]
            Redis cache to store the image

        Return
        ------
        image : PDS3Image
            Image from the url
        """

        name = cls._get_name_from_url(url)
        content = cls._get_content(url, rcache)
        image = cls(
            stream_string_or_array=BytesIO(content),
            filename=name,
            compression='url',
            url=url,
            rcache=rcache,
        )
        return image

    def __init__(self, stream_string_or_array, filename=None, compression=None,
                 url=None, rcache=None):
        self._url = url
        self._rcache = rcache
        super().__init__(
            stream_string_or_array=stream_string_or_array,
            filename=filename,
            compression=compression,
        )

    @property
    def url(self):
        return self._url

    @property
    def data_url(self):
        return self.url.replace(self.filename, self.data_filename)

    def _load_detached_data(self):
        if self.url is not None:
            content = self._get_content(self.data_url, self._rcache)
            return self._decode(BytesIO(content))
        else:
            return super()._load_detached_data()

    @property
    def _decoder(self):
        if self.format == 'BAND_SEQUENTIAL':
            return BandSequentialDecoder(
                self.dtype, self.shape, self.compression
            )
        raise ValueError('Unkown format (%s)' % self.format)


app = Flask(__name__)


def cache_image(url):
    logger.info(url)
    rcache = Redis(host=REDIS_HOST)
    name = url.split('/')[-1]
    if rcache.hexists('image', name):
        logger.info(f'{name} exists')
        rcache.set('progress', 100)
        return
    else:
        content = b''
        progress = 0
        logger.info('getting image')
        with requests.get(url, stream=True) as r:
            size = float(r.headers['Content-Length'])
            chunk = int(size // 100) or 1
            for data in r.iter_content(chunk_size=chunk):
                progress += len(data)
                logger.info((progress / size) * 100)
                rcache.set('progress', (progress / size) * 100)
                content += data
        logger.info('Setting Cache')
        rcache.hset('image', name, content)
        return


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/_get_progress')
def _get_progress():
    rcache = Redis(host=REDIS_HOST)
    logger.info('getting progress')
    progress = rcache.get('progress')
    progress = progress if progress is not None else 0
    return jsonify(progress=float(progress))


@app.route("/_cache_image", methods=['POST'])
def _cache_image():
    url = request.json.get('url')
    thread = threading.Thread(target=cache_image, kwargs={'url': url})
    thread.start()
    return jsonify(caching=True)


@app.route("/_get_image")
def _get_image():
    """

    Special thanks to this gist for posting an image using flask:
    https://gist.github.com/wilsaj/862153
    """

    logger.info('displaying image')
    url = request.args.get('url')
    fig = Figure()
    ax = fig.add_subplot(111)
    rcache = Redis(host=REDIS_HOST)
    rcache.set('progress', 0)
    image = PDS3Image.open_url(url, rcache)
    if image.image.ndim == 2:
        cmap = 'gray'
    else:
        cmap = None
    fig.patch.set_visible(False)
    ax.imshow(image.image, cmap=cmap)
    ax.axis('off')
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == "__main__":
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    app.run(host=HOST, port=PORT, threaded=True)
