import emoji


# print(emoji.emojize('Python is :thumbs_up_sign:'))

word = 'ยินดีที่ในวันนั้นฉันได้รู้ตัว💙😍🎉🎊👿🎂🐰 💓❤💕 🎂🎈 💛🎁🐰😭🔥🙏'

if '\U0001f495' in word:
    print('🙏')
else:
    print('no')
