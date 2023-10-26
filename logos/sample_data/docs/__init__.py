import glob
from pathlib import Path

dir_path = Path(__file__).parent

def get_sample_docs():
    doc_files = glob.glob(str(dir_path / 'eden/*.md'))
    docs = []

    for doc_file in doc_files:
        with open(doc_file, 'r') as file:
            docs.append(file.read())

    return docs

def get_cached_eden_summary():
    return cached_summary

cached_summary = [
    "This document provides a comprehensive guide on how to train and use custom concepts in Eden's generative model, SDXL. It explains the process of training a new concept by uploading images to the concept trainer, waiting for the training to finish, and then using the concept in the creation tool. The document covers three training modes: concept, face, and style, and provides detailed instructions on how to generate with concepts. It also provides examples of each mode and discusses the importance of the quality and diversity of training images. The document further explains the required and advanced parameters for training, and offers tips and tricks for successful concept training.",
    "This document provides a comprehensive guide to the Eden App, a platform that offers various AI-powered image and video creation endpoints. The document covers seven main endpoints: Create, ControlNet, Interpolate, Real2Real, Remix, Blend, and Upscale. The Create endpoint allows users to generate images from text prompts, while ControlNet enables style transfer from a guidance image. Interpolate and Real2Real are video endpoints that generate smooth transition videos from multiple prompts or images, respectively. Remix creates variations of an input image, Blend combines two images, and Upscale enhances the resolution of an image. Each endpoint's functionality, usage, and optional settings are detailed in the document",
    "This document provides instructions on how to use the Eden SDK, a JavaScript library for interacting with the Eden API. It covers how to obtain API credentials, the installation process of the SDK, and how to make a creation request using the `EdenClient` class. It also provides an example of how to poll a task until it is completed. The document further explains how to retrieve a user's Manna balance using the SDK. It also mentions that the SDK is available as an npm package and that a commonjs version and Python SDK are planned for the future. Lastly, it notes that there is currently no way to retrieve the cost in Manna of a specific config or job requests.",
    "This document provides an overview of Eden, a platform designed to make expressive generative AI tools accessible to creators. Eden's flagship product is a social network that allows creators to generate, share, and remix art, train custom models, and deploy interactive agents and chatbots. The document is divided into two sections: guides for creators and a technical reference. The guides cover how to use the creation tool, train custom models, and deploy characters. The technical reference introduces the Eden API and SDK, and provides a guide for hosting custom models or code. The document also discusses Eden's mission, core principles, and the problems it aims to solve. Lastly, it introduces Manna, Eden's internal currency, and explains how to acquire it."
]
