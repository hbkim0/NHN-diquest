"use strict";

const BASE_URL = process.env.VUE_APP_IMAGE_BASE_URL || '';

function resolveImageUrl(image_url) {
    if ((typeof(image_url) !== 'string') || (!image_url)) {
        return '';
    }

    const url = new URL(image_url, BASE_URL);
    return url.toString();
}

export {
    resolveImageUrl
};