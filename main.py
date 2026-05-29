#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[RU]
Главный модуль UDP чата.

[EN]
Main UDP chat module.
"""

import sys
import locale
from queue import Queue
import time
from args import parse_args
from net import UdpReceiverThread, UdpSenderThread


def main():
    """
    [RU]
    Главная функция приложения с двумя потоками.
    
    Аргументы:
        None: Функция не принимает аргументов.
        
    Возвращает:
        None: Функция не возвращает значение.
        
    [EN]
    Main application function with two threads.
    
    Args:
        None: Function does not accept arguments.
        
    Returns:
        None: Function does not return a value.
    """
    receiver_thread, sender_thread = None, None

    try:
        # Настройка локализации для поддержки кириллицы
        locale.setlocale(locale.LC_ALL, '')

        # Разбор аргументов командной строки
        args = parse_args()

        # Создание очереди для сообщений
        message_queue = Queue()

        # Создание потоков (приемник и отправитель)
        receiver_thread = UdpReceiverThread(message_queue, args.ip, args.port)
        sender_thread = UdpSenderThread(message_queue, args.ip, args.port)

        # Запуск потоков
        receiver_thread.start()
        sender_thread.start()

        # Информационный вывод
        print(f"Запуск чата на {args.ip}:{args.port}")
        print("Нажмите Ctrl+C для выхода")

        # Ожидание завершения потоков
        while receiver_thread.is_alive() or sender_thread.is_alive():
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nПолучен сигнал прерывания. Завершение...")

        # Завершение потоков
        if 'receiver_thread' in locals():
            receiver_thread.stop()
        if 'sender_thread' in locals():
            sender_thread.stop()

        # Ждем завершения с таймаутом
        if 'receiver_thread' in locals():
            receiver_thread.join(timeout=2)
        if 'sender_thread' in locals():
            sender_thread.join(timeout=2)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    finally:
        # Дополнительная очистка
        try:
            # Финальная попытка аккуратно остановить потоки
            if 'receiver_thread' in locals() and receiver_thread.is_alive():
                receiver_thread.stop()
                receiver_thread.join(timeout=1)
            if 'sender_thread' in locals() and sender_thread.is_alive():
                sender_thread.stop()
                sender_thread.join(timeout=1)
        except:
            pass
        print("Чат завершен.")


if __name__ == "__main__":
    main()
