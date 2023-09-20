

"""
1. Нужно прочитать файл с субтитрами:
2. Перебрать его в цикле:
    1. Озвучить каждую реплику
    2. Сохранить синтезированную запись в файл  E:\bg3-modders-multitool\UnpackedData\Voice\Localization\Russian\Soundbanks\файл.wav

3. Через Wwise конвертировать wav в wen:
    1. Сохранить синтезированную запись в файл  E:\bg3-modders-multitool\UnpackedData\Voice\Localization\Russian\Soundbanks\файл.wem

4. Упаковать озвучку в .pak
5. Заменить Voice.pak
"""
"""

Вечеринки у гоблинов гораздо веселее любых праздников во Вратах Балдура. Да и в аду тоже.


hcb228250g01eeg4e3cg88abg3f55fb87ee71 -> v2c76687d93a2477b8b188a14b549304c_hcb228250g01eeg4e3cg88abg3f55fb87ee71.wav

v2c76687d93a2477b8b188a14b549304c_hcb228250g01eeg4e3cg88abg3f55fb87ee71.wav -> v2c76687d93a2477b8b188a14b549304c_hcb228250g01eeg4e3cg88abg3f55fb87ee71.wem
"""

"""
Распаковка .PAK-файлов Baldur's Gate 3 и упаковка их обратно - https://steamcommunity.com/sharedfiles/filedetails/?id=2381865525
Как преобразовать файлы WEM в воспроизводимый звук WAV, OGG и MP3 - https://www.gaminghouse.community/en/guides-tutorials-1003/how-to-play-convert-wem-files-ogg-mp3-67
Converting Wav to Wem with WWise - https://www.youtube.com/watch?v=39Oeb4GvxEc&t=126s
Скачать audiokinetic -https://www.audiokinetic.com/en/thank-you/launcher/windows/?ref=download&platform=1
Скачать vgmstream - https://github.com/vgmstream/vgmstream/releases
Техническое руководство для работы с файлами Baldur's Gate III - https://raidgame.ru/threads/texnicheskoe-rukovodstvo-dlja-raboty-s-fajlami-baldurs-gate-iii.616/#post-935
"""

"""
Для создания pack:
- Выбирать No compression
- Выбирать solid

Нужно скидывать в игру два .pak

e:\Baldurs Gate 3\Data\Localization\Voice.pak 
e:\Baldurs Gate 3\Data\Localization\Voice_1.pak
"""

"""
TODO:

Работает подмена дорожек.

теперь нужно найти способ чтобы свои озвучки работали, так как сейчас это просто тишина


Вопрос на Stack Overflow - https://stackoverflow.com/questions/76963375/baldurs-gate-3-how-to-convert-wav-to-wav-correctly

"""