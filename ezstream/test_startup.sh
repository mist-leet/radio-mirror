#!/bin/bash

curl -X GET --location "http://0.0.0.0:8888/internal/create_and_run";

curl -X GET --location "http://0.0.0.0:8888/internal/main/update" \
    -H "Content-Type: application/json" \
    -d "[
        \"/source/2006 - Сквозное (EP)/01. Хочешь.mp3\",
        \"/source/2006 - Сквозное (EP)/02. Приоритеты.mp3\",
        \"/source/2006 - Сквозное (EP)/03. Простые слова.mp3\",
        ]";