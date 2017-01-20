# #CheeseMilkTomatoRobot

 #CheeseMilkTomatoRobot - это удивительная нейросеть, способная классифицировать изображения скоропортящейся продукции.

На данный момент поддерживаются три класса:

0. Сыр
1. Молоко
2. Томаты

### Протестировать работу
- Перейдите на наш [сайт](http://46.101.155.29:8080/)
- Вставьте в поле ссылку на jpg-изображение и нажмите Guess! 
- Несколько примеров ссылок, можете начать с них:
 - Сыр: http://static.medportal.ru/pic/mednovosti/news/2015/10/26/106cheese/shutterstock_224608219_small_500x375.jpg
 - Молоко: http://eco-boom.com/wp-content/uploads/2013/07/moloko-300x200.jpeg
 - Томат: https://wallpaperscraft.ru/image/pomidory_vetka_orehi_70700_1080x1920.jpg 
 
### Результаты
![N|Solid](https://pp.vk.me/c604325/v604325426/528a3/UhPIRWko7i8.jpg)

### Обучение сети
- Склонируйте репозиторий: 
```sh
$ git clone https://github.com/GuminEgor/CheeseMilkTomatoRobot.git
```
- Скачайте [датасет](https://drive.google.com/file/d/0B05H_bVIKg-JQW1OVGktQUhkeGs/view?usp=sharing)
-  Распакуйте архив и поместите папку data на одном уровне с train.py (этот файл находится в директории net)
-  Запустите:
```sh
$ python3 train.py
```

### Запуск веб-сайта и предсказания
- Если хотите использовать веса, которые посчитали сами - скопируйте файл 3classes_with_augmentation.h5 в папку website
- Запустите
```sh
$ python3 server.py
```
- Откройте http://localhost:8080/

### Дополнительная информация
Сайт разрабатывался как чисто демонстрационный и не рассчитан на высокую нагрузку и ковыряние в дырках на тему безопасности. Тем не менее, будем рады пулл-реквестам и сообщениям на почту на тему "как это исправить".
