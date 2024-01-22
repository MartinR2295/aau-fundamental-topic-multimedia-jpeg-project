import cv2


def compress(y, u, v, scaling_factor):
    u_downscaled = cv2.resize(u, (u.shape[1] // scaling_factor, u.shape[0] // scaling_factor))
    v_downscaled = cv2.resize(v, (v.shape[1] // scaling_factor, v.shape[0] // scaling_factor))

    # TODO: do the y part
    # TODO: split y part to 8x8 blocks

    # TODO: do dct to each block

    # TODO: do quantization to each block

    return y, u_downscaled, v_downscaled


def decompress(y_compressed, u_downscaled, v_downscaled):
    # Upscale the U component
    u = cv2.resize(u_downscaled, (y_compressed.shape[1], y_compressed.shape[0]))
    # Upscale the V component
    v = cv2.resize(v_downscaled, (y_compressed.shape[1], y_compressed.shape[0]))

    # do the y part
    y = y_compressed

    return y, u, v
