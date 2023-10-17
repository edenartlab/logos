## Overview
If you havent already, go to the **[Eden App](https://app.eden.art/)** and login with your email to get started!
Before diving into each of Edens endpoints separately, lets do a quick overview of what each one does:

#### Image endpoints:
- **Create** is our *'text-to-image'* pipeline, allowing you to create images from prompts using [SDXL](https://stability.ai/stablediffusion) (StableDiffusion XL)
- **ControlNet** lets you 'style-transfer' a guidance image using prompts
- **Blend** takes two images and creates a blend of them.
- **Upscale** upscales a single image to a higher resolution.
- **Remix** takes a single image and creates variations of it (prompts are optional).

#### Video endpoints:
- **Interpolate** is an extension of create where you enter multiple prompts and get a interpolation video back that morphs through those prompts
- **Real2Real** is like Interpolate, but instead of prompts, it start from images only. You upload a sequence of images and real2real will generate a smooth video morph between your images!

Most of these endpoints are fairly easy to use with just the default settings, but getting good results with AI requires some of understanding about what goes on under the hood, so let's dive in!

## 1. /create

**[Create](https://app.eden.art/create/creations)** is our *text-to-image* endpoint, powered by StableDiffusion XL. Set your desired image resolution, enter your prompt and hit create, simple as that!

If you’re the first person to trigger a creation job in a while, it is possible that our backend will spin up a new gpu-box for you, which might take a few minutes. Once a gpu is up and running, image creations should take around 5-10 seconds with default settings.

### Optional settings
Every one of our endpoints has a dropdown *'Show optional settings'* that offers a ton of additional features. Lets go over them:

- ***'Width'*** and ***'Height'*** set the amount of pixels and aspect ratio of your creation. Note that if you are using init images or doing real2real, the generator will automatically adopt the aspect ratio of your inputs and distribute the total amount of pixels (width x heigth) over that aspect ratio.
- ***'Upscale Factor'*** wil upscale the resolution of your generated image by the given factor after generating it with SDXL. If you want very HD images, upscaling is generally better than simply rendering at higher starting resolutions (width and height). This is because the model is trained for a specific resolution and going too far beyond that can create repeating artifacts in the image, but feel free to experiment here!
- ***'concept'*** and ***'concept-scale'*** allow you to activate a trained concept in your creation, one of the most powerful features on Eden. See our **[concept-trainer guide](https://docs.eden.art/docs/guides/concepts)** for all the details!
- ***'ControlNet or Init image'*** let’s you upload an image that the model will use as a color and shape template to start drawing from. This allows much more control over what the final image should look like.
- The ***‘Init image strength’*** controls how heavily this init image influences the final creation. SDXL is very sensitive to init_images so you usually want to set low values, a good first value to try is 0.2 Values above 0.5 will look almost identical to your init image.
- ***'samples'*** allows you to generate multiple variations with a single job.
- ***'negative prompt'*** allows you to specify what you DONT want to see in the image. Usually keeping this at default is fine, but feel free to experiment!
- ***'guidance scale'*** how strongly the prompt drives the creation. Higer values usually result in more saturated images.
- ***'sampler'*** the diffusion sampler to use, see [here](https://huggingface.co/docs/diffusers/v0.20.0/en/api/schedulers/overview)
- ***'steps'*** how many denoising steps to use. Higher values will be slower but sometimes produce more details. Strong diminishing returns past 40 steps.
- ***'seed'*** random seed for reproducibility. Fixing the seed can make it easier to determine the precise effect of a certain parameter while keeping everything else fixed.

## 2. /controlnet
Controlnet allows you to adopt the shape / contours of a control image into your creation, but still apply the style and colors with a text prompt.
The best way to understand controlnet is to just show it:

#### Step 1: Upload your control image:
Input: the original logo for Abraham, our autonomous digital artist

#### Step 2: Pick your controlnet type ("canny-edge" or "depth" currently supported)
This will cause different kinds of controlnet conditioning:
  - canny-edge will try to produce a creation that has the same canny-edge map as your control image
  - depth will try to produce a creation that has the same depth map as your control image
  - luminance will try to mimic the bright and dark regions in your control image, it is probably the best controlnet model.
Experiment!

#### Step 3: Set the init image strength
This value controls how strongly the control image affects the creation.  
Usually values between and 0.4-0.8 are good starting points.

## 3. /interpolate
Interpolate lets you create smooth interpolation video’s by entering a sequence of prompts. This allows you to create simple, linear video narratives and is fully compatible with **[custom concepts](https://docs.eden.art/docs/guides/concepts)**. Here’s a simple videoloop between the following prompts:
    - "a photo of a single lone sprout grows in a barren desert, the horizon is visible in the background, low angle 8k HD nature photo"
    - "a photo of a lone sappling growing in a field of mud, realistic water colour"
    - "a photo of a huge, green tree in a forest, the tree is covered in moss, 8k HD nature photo"
    - "a photo of an old, crumbled Tree of life, intricate wood folds, 8K professional nature photography, HDR"

### Lerp + ControlNet:

Just like with /Create, you can use an Init image combined with ControlNet "canny-edge" to create an interpolation video guided by a control image:
<iframe width="500" height="500" src="https://storage.googleapis.com/public-assets-xander/A_workbox/eden_docs/eden_lerp.mp4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

The above was created with the Abraham logo as init image and a controlnet image strength of 0.65

## 4. /real2real

**Real2Real** is an algorithm we’re pretty proud of. It essentially does the same as lerp, except that here, the input is not a sequence of prompts, but a sequence of arbitrary images. The algorithm will then create a smoothed video interpolation morphing between those real input images, no prompt engineering required.

Real2Real accepts ANY input image, so you can eg import images from MidJourney, use photographs, sketches, video frames, …

Below is an example of a Real2Real morphing between the following input images:

Note that while Real2Real accepts litterally any input image, the quality of the interpolation will depend on how well the generative model can represent the input images. Eg StableDiffusion was not particularly trained on faces and so Real2Real tends to give underwhelming results on face interpolations.

Like our other endpoints, Real2Real has a few customization parameters that can dramatically affect the results from this algorithm:

- ***'FILM iterations'***: when set to 1, this will post-process the video frames using FILM, dramatically improving the smoothness of the video (and doubling the number of frames).
- ***'Init image min strength'***: the minimum strength of the init_imgs during the interpolation. This parameter has a significant effect on the result: low values (eg 0.0–0.20) will result in interpolations that have a longer “visual path length”, ie: more things are changing and moving: the video contains more information at the cost of less smoothness / more jitter. Higher values (eg 0.20–0.40) will seem to change more slowly and carry less visual information, but will also be more stable and smoother.
→ Experiment and see what works best for you!
- ***'Init image max strength'***: the maximum strength of the init_imgs during the interpolation. Setting this to 1.0 will exactly reproduce the init_imgs at the keyframe positions in the interpolation at the cost of a brief flicker (due to not being encoded+decoded by VQGAN). Setting this to lower values (eg 0.70–0.90) will give the model some freedom to ‘hallucinate’ around the init_img, often creating smoother transitions. Recommended values are 0.90–0.97, experiment!

## 5. /remix

Remix does exactly what you think it does: it takes an input image and creates a variation of it. Internally, remix will try to construct a prompt that matches your image and use it to create variations of your image with.

The most important parameter here is:

- Init image strength: controls how much influence the init image has over the final result. Setting this to 0.0 will produce a remix that is entirely based on the ‘guessed prompt’ for the image and not influenced at all by the actual colors / shape of the input image. This could produce more creative images but will diverge more from the original.

## 6. /blend
Blend takes two input images and will produce a blended / mixed version of them as output.

## 7. /upscale
Upscale takes a single input image and will produce an upscaled version of it. The parameters are:
- ***'Init image strength'*** how strongly to use the original image. Lower values give the upscaler more freedom to create new details, often leading to a sharper final image, but will also deviate more from the original. Recommended values are 0.3-0.7
