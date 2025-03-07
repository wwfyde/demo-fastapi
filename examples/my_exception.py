def main():
    try:
        do_some()
    except:
        print("do_some error")
    else:
        print("do_some success")
    finally:
        print("do_some finally")


if __name__ == "__main__":
    main()
