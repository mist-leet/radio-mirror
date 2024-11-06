#!/bin/bash

# Проверяем, что был передан путь к файлу
if [ -z "$1" ]; then
    echo "Ошибка: Укажите путь к .txt файлу как первый аргумент."
    exit 1
fi

# Проверяем, что указанный файл существует
if [ ! -f "$1" ]; then
    echo "Ошибка: Файл $1 не найден."
    exit 1
fi

# Читаем первые пять строк из файла и обрабатываем каждую
count=0
while IFS= read -r line && [ "$count" -lt 5 ]; do
    # Извлекаем директорию из пути файла
    dir=$(dirname "$line")

    # Проверяем, что директория существует, и переходим в нее
    if [ -d "$dir" ]; then
        echo "Переходим в директорию: $dir"
        cd "$dir" || exit 1
    else
        echo "Предупреждение: Директория $dir не найдена."
    fi

    ((count++))
done < "$1"
