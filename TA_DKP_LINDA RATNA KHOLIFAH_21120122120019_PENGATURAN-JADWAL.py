import PySimpleGUI as sg
from plyer import notification
import tkinter as tk
from tkinter import messagebox

class ScheduleManager:
    def __init__(self):
        self.schedule_list = []
        self.quick_note_list = []
        self.reading_list = []
        #buat tata letak GUI
        self.layout = [
            [sg.Column([
                [sg.Text('Schedule Settings', font=('Helvetica', 20), justification='center')]
            ], element_justification='center')],
            [sg.TabGroup([
                [
                    #Menambahkan elemen GUI untuk tab planner
                    sg.Tab('Planner', [
                        [sg.Text('Nama Kegiatan', size=(15, 1)), sg.InputText(key='Nama')],
                        [sg.Text('Kategori', size=(15, 1)), sg.Combo(['Important', 'Not Important'], key='Kategori')],
                        [sg.Text('Tanggal', size=(15, 1)), sg.InputText(key='Tanggal'),
                         sg.CalendarButton('Kalender', target='Tanggal', format=('%d-%m-%Y'))],
                        [sg.Text('Jam', size=(15, 1)), sg.Spin([str(i).zfill(2) for i in range(24)], initial_value='00', size=(2, 1), key='Jam'),
                         sg.Text(':', size=(1, 1)), sg.Spin([str(i).zfill(2) for i in range(60)], initial_value='00', size=(2, 1), key='Menit')],
                        [sg.Table(values=self.schedule_list, headings=['Nama Kegiatan', 'Kategori', 'Tanggal', 'Jam'],
                                  justification='center', key='table')],
                        [
                            sg.Column([
                                [sg.Button('Add'), sg.Button('Clear'), sg.Button('Update'), sg.Button('Delete')],
                            ], justification='right')
                        ]
                    ]),
                    #Menambahkan elemen GUI untuk tab quick note
                    sg.Tab('Quick Note', [
                        [sg.Multiline(key='note_input', size=(40, 5))],
                        [sg.Button('Add Note')],
                        [sg.Listbox(values=self.quick_note_list, size=(40, 5), key='quick_note_list')],
                        [sg.Button('Delete Note')]
                    ]),
                    #Menambahkan elemen GUI untuk tab reading list
                    sg.Tab('Reading List', [
                        [sg.InputText(key='book_input', size=(30, 1)), sg.Button('Add Book')],
                        [sg.Listbox(values=self.reading_list, size=(40, 5), key='reading_list')],
                        [sg.Button('Delete Book')]
                    ])
                ]
            ])]
        ]
        #create the window
        self.window = sg.Window('Pengaturan Jadwal', self.layout)
        self.run()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    def set_input_values(self, values):
        self.window['Nama'].update(values.get('Nama', ''))
        self.window['Kategori'].update(values.get('Kategori', ''))
        self.window['Tanggal'].update(values.get('Tanggal', ''))
        self.window['Jam'].update(values.get('Jam', '00'))
        self.window['Menit'].update(values.get('Menit', '00'))

    def get_input_values(self):
        return {
            'Nama': self.window['Nama'].get(),
            'Kategori': self.window['Kategori'].get(),
            'Tanggal': self.window['Tanggal'].get(),
            'Jam': self.window['Jam'].get(),
            'Menit': self.window['Menit'].get(),
        }

    #Perulangan tersebut akan terus berjalan selama tidak ada event yang terjadi 
    # atau window tidak ditutup.
    def run(self):
        while True:
            event, values = self.window.read() #akan membaca event dan nilai dari elemen-elemen GUI yang ada di jendela

            if event == sg.WINDOW_CLOSED: #perulangan akan berhenti dengan `break`. Sebaliknya, jika event lain terjadi, program akan melanjutkan eksekusi untuk menangani event tersebut.
                break

            if event == 'Add':
                new_schedule = self.get_input_values()
                new_schedule['Jam'] += ':' + new_schedule['Menit']  # Concatenate 'Jam' and 'Menit' values
                del new_schedule['Menit']  # Remove 'Menit' key
                self.schedule_list.append(new_schedule)
                self.window['table'].update(values=[list(schedule.values()) for schedule in self.schedule_list])
                self.show_notification(new_schedule['Nama'], new_schedule['Tanggal'], new_schedule['Jam'])
                messagebox.showinfo('Info', 'Jadwal berhasil ditambahkan')

            if event == 'Delete':
                selected_rows = self.window['table'].SelectedRows
                if selected_rows:
                    for index in sorted(selected_rows, reverse=True):
                        del self.schedule_list[index]
                    self.window['table'].update(values=[list(schedule.values()) for schedule in self.schedule_list])
                    messagebox.showinfo('Info', 'Jadwal berhasil dihapus')

            if event == 'Clear':
                self.set_input_values({})

            if event == 'Update':
                selected_rows = self.window['table'].SelectedRows
                if selected_rows:
                    row_index = selected_rows[0]
                    schedule = self.schedule_list[row_index]
                    self.set_input_values(schedule)
                    del self.schedule_list[row_index]
                    self.window['table'].update(values=[list(schedule.values()) for schedule in self.schedule_list])
                    messagebox.showinfo('Info', 'Jadwal berhasil diperbarui')

            if event == 'Add Note':
                note_text = self.window['note_input'].get()
                if note_text:
                    self.quick_note_list.append(note_text)
                    self.window['quick_note_list'].update(values=self.quick_note_list)
                    self.window['note_input'].update(value='')
                    messagebox.showinfo('Info', 'Catatan cepat berhasil disimpan')

            if event == 'Delete Note':
                selected_notes = self.window['quick_note_list'].get()
                if selected_notes:
                    for note in selected_notes:
                        self.quick_note_list.remove(note)
                    self.window['quick_note_list'].update(values=self.quick_note_list)
                    messagebox.showinfo('Info', 'Catatan cepat berhasil dihapus')

            if event == 'Add Book':
                book_title = self.window['book_input'].get()
                if book_title:
                    self.reading_list.append(book_title)
                    self.window['reading_list'].update(values=self.reading_list)
                    self.window['book_input'].update(value='')
                    messagebox.showinfo('Info', 'Buku berhasil ditambahkan')

            if event == 'Delete Book':
                selected_books = self.window['reading_list'].get()
                if selected_books:
                    for book in selected_books:
                        self.reading_list.remove(book)
                    self.window['reading_list'].update(values=self.reading_list)
                    messagebox.showinfo('Info', 'Buku berhasil dihapus')

        self.window.close()

    def show_notification(self, nama_kegiatan, tanggal, jam):
        notification_title = 'Jadwal Baru'
        notification_message = f'Kegiatan: {nama_kegiatan}\nTanggal: {tanggal}\nJam: {jam}'
        notification.notify(title=notification_title, message=notification_message)

schedule_manager = ScheduleManager()
