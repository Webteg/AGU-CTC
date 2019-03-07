from python3_anticaptcha import NoCaptchaTaskProxyless
from python3_anticaptcha import ImageToTextTask

def solveCaptcha(PAGE_URL):

    ANTICAPTCHA_KEY = "cfff02538f8b393ab3df35257154f982"
    SITE_KEY = '6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'
    user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(websiteURL=PAGE_URL,websiteKey=SITE_KEY)
    
    return user_answer

def ImageCaptcha(image_link):
    ANTICAPTCHA_KEY = "cfff02538f8b393ab3df35257154f982"

    try:
        user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(captcha_file=image_link)
        if user_answer['errorId'] == 0:
            return user_answer['solution']['text']

        elif user_answer['errorId'] == 1:
            return user_answer['errorBody']
    except Exception as erro:
        return erro