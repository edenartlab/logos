### **Summary**
1. Train a new concept by uploading images to the [concept trainer](https://app.eden.art/create/concepts) and picking a training mode.
2. Wait for training to finish (takes 5-10 mins)
3. Go to the [creation tool](https://app.eden.art/create/creations) (/create, /interpolate or /real2real)
4. Select your concept from the concept dropdown menu
5. Trigger the concept by adding <concept\> in your prompt text (not needed for styles & real2real):  
eg ***"a photo of <concept\> climbing a mountain"***
6. **If things dont look good, instead of messing with the settings, try changing your training images: they're the most important input variable!**

## Introduction
**Concepts** are custom characters, objects, styles, or specific people that are not part of the base generative model's (SDXL) knowledge, but that can be trained into the model by showing it a few examples of your concept. Once trained, you can naturally compose with concepts in your prompts just like you'd normally do with things the model knows already, eg a person named 'Barack Obama' or a style like 'cubism'.

Concepts are first trained by uploading example images to the [concept trainer](https://app.eden.art/create/concepts). After training finishes (this takes about 5 mins), the concept becomes available to use in the main creation tool and is compatible with single image creates, interpolations and real2real. Note that a concept has to be:
- activated in the creation by selecting the corresponding name from the concept dropdown menu
- triggered by using <concept\> to refer to it in the prompt text.

Concepts are a highly versatile and powerful creation tool. They can be used to capture a specific person's face or likeness, an animated character, or a complex object. They can also be more abstract, referring to a particular artistic style or genre.

## Training

The concept trainer is available at [https://app.eden.art/create/concepts](https://app.eden.art/create/concepts) and is a rework of the great LORA trainer created by [@cloneofsimo](https://twitter.com/cloneofsimo) over [here](https://github.com/replicate/cog-sdxl).

To train a good concept you need just a few (3-10 images is fine), but really good training images. Really good in this context means:
- good resolution (at least 768x768 pixels is recommended)
- diverse (it's better to have 5 very diverse images than 20 almost identical ones)
- well cropped, clearly showing the concept you're trying to learn

The training images are the most important part of concept training, if things dont look good, instead of changing the settings, just try a different (sub-) set of training images!

## Generating with concepts:

Once a concept has been trained, here's how to use it:
1. Select your trained concept from the concept dropdown menu in the creation tool:

2. If the concept was trained with "style" mode you can prompt as normal. If the concept was trained with "face" or "concept" mode, you have to trigger your concept/face in the prompt. There are two options to do this:
   - You can either trigger your concept by referring to it as <concept\> in your prompt text, eg  
   ***"a photo of <concept\> climbing a mountain"***
   - Or you can use the actual name of your trained concept. Eg if my concept name was "Banny" I could prompt-trigger it like so:  
   ***"a photo of <Banny\> climbing a mountain"***

3. When generating you can adjust the concept scale, which will control how strongly the concept is being used in the generation. 0.8 is usually perfect (1.0 usually doesn't work so well!), but in some cases, when the concept is slightly overfit, you can try to lower this value to get more promptability.

Note: all the example images in this post were generated with the default trainer & generation settings!

## Examples
### Example: face-mode

Generative models like Stable Diffusion are great at generating realistic faces. However, the model obviously doesn't know what everyone looks like (unless you are very famous). To get around this, we can train a concept to learn a specific person's face.
When training "face" concepts it is recommended to disable the random left/right flipping of training images (see more details below under **"advanced parameters"**).

For example, the training samples below are of [Xander](https://twitter.com/xsteenbrugge).

After training, we can use the concept <Xander\> in a prompt to generate realistic and figurative pictures:
- <Xander\> as a character in a noir graphic novel
- <Xander\> action figure
- <Xander\> as a knight in shining armour
- <Xander\> as the Mona Lisa
- etc ...

Faces are a popular and easy use case. It is possible to learn a face accurately from a single image, although two or three images are usually recommended to provide a bit of additional diversity.

### Example: concept-mode

**Concepts** can also be used to model consistent objects or characters. The above images are professional renders of the character for our Kojii project. This is a good example of a great training set since it contains: a single, consistent character with subtle variations in pose and appearance between every image. After training a new concept with name "kojii" with mode 'concept' and default settings, we get a fully promptable Kojii character, eg (see top image row):
- a photo of <kojii\> surfing a wave
- <kojii\> in a snowglobe
- a low-poly artwork of <kojii\>
- a photo of <kojii\> climbing mount Everest, alpinism
- etc ...

### Example: style-mode

Concepts can also be used to model artistic styles. For example, the following training samples below are artworks originally created by [VJ Suave](https://vjsuave.com/).

You can then train a concept using the "style" mode, and generate with it in /create. For style concepts, you dont even have to trigger the concept in any way, just prompt like you normally would.
The following are samples are all generated from the trained Suave concept (using default settings for both the trainer and creations):

## Training parameters

### Required parameters:

* **Concept name**: The name of the concept. This can be used to refer to the concept in prompts. Names are not required to be unique and can be reused.
* **Training images**: The images to use for training. You can upload image files (jpg, png, or webm), or you can upload zip files containing multiple images. You may upload up to 10 files, and each file must be below 100MB. From our experiments, the concept training actually works best if you dont have too many images. We recommend using 3-10 high quality and diverse images.
* **Training mode**: There are three available modes: concept, face, and style. They refer to trainer templates that are optimized for these three categories. Faces refer to human faces, concepts may refer to objects, characters, or other "things," while styles refer to the abstract style characteristics common to all the training images. Select the one that best matches your training set.

The trainer is designed to handle most cases well with the default settings, particularly in the case of concepts. Some concepts and  styles are more challenging to capture well and may require some trial and error adjusting the optional settings to achieve the right balance of diversity, accuracy, and promptability. To give some intuitions about how the advanced settings may affect the results, we describe them below. 

However keep in mind that **the most important input parameter are the training images themselves**: if things dont look good, instead of spending hours fiddling with the advanced parameters, we highly recommend to first try training again with a different subset of your images (using default parameters).

### Advanced parameters:

* **Number of training steps**: This refers to how long to finetune the model with your dataset. More steps should lead to fitting your concept more accurately, but too much training may "overfit" your training data, leading the base model to "forget" much of its prior knowledge (prompting wont work well anymore) and produce visual artifacts.
* **To randomly flip training imgs left/right**: This setting doubles the number of training samples by randomly flipping each image left/right. This should generally be on, unless the object you want to learn has a specific horizontal orientation which should not appear mirrored (for example text (LOGO's) or faces).
* **Learning rate for the LORA matrices**: The learning rate for the LORA matrices that adjust the inner mechanics of the generative model to be able to draw your concept. Higher values lead to 'more/faster learning' usually leading to better likeness at the cost of less promptability. So if the creations dont look enough like your training images --> try increasing this value, if your images dont listen to your prompts --> try decreasing this value.
* **Learning rate for textual inversion phase** : Textual inversion refers to the part of the training process which learns a new dictionary token that represents your concept. So in the same way that StableDiffusion knows what a "table" is and can draw tables in many different forms and contexts, it will learn a new token that represents your concept.
* **LORA rank** : Higher values create more 'capacity' for the model to learn and can be more succesful for complex objects or styles, but are also more likely to overfit on small image sets. The default value of 4 is recommended for most cases.
* **trigger text** : Optional: a few words that describe the concept to be learned (e.g "man with mustache" or "cartoon of a yellow superhero"). Giving a trigger text can sometimes help the model to understand what it is you're trying to learn and tries to leverage prior knowledge available in the model. When left empty, the trigger text will be automatically generated (recommended).
* **Resolution** : Image resolution used for training. If your training resolution is much lower than the resolution you create with, the concept will appear smaller inside your larger image and will often have repeating artefacts like multiple noses or copies of the same face. Training at lower resolutions (eg 768) can be useful if you want to learn a face but want to prompt it in a setting where the face is only a small part of the total image. Using init_images with rough shape composition can be very helpful in this scenario.
* **Batch size** : Training batch size (number of images to look at simultaneously during training). Increasing this may lead to more stable learning, however all the above values have been finetuned for batch_size = 2. Adjust at your own risk!

# Tips & trics

:::tip
- the advanced settings are pretty well optimized and should work well for most cases.
- When things dont look good: try changing your training images before adjusting the settings!
:::tip

:::warning
- When uploading face images, it's usually a good idea to crop the images so the face fills a large fraction of the total image.
- We're used to "more data is always better", but for concept training this usually isn't true: 5 diverse, HD images are usually better than 20 low-quality or similar images.
:::warning