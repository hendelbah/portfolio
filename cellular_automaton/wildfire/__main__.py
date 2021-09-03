from wildfire.tk_ui import tk, Application


def main():
    root = tk.Tk()
    root.title('Cellular automatons: Wildfire')
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
