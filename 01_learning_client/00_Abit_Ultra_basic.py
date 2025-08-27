def main():
    file = None
    try:
        file = open("open.txt", 'r')
        output = file.readlines()
    except FileNotFoundError as e:
        print(e)
    finally:
        if file is not None:
            file.close()

if __name__ == "__main__":
    main()