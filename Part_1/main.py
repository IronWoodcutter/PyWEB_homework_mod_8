from pprint import pprint
from hw import find_by_tag, find_by_tags, find_by_author


def main():
    while True:
        user_input = input("Enter query(command:values) or exit: ")
        if user_input == 'exit':
            break
        try:
            command, value = user_input.split(':')
            value = value.strip()
            match command:
                case 'tag':
                    pprint(find_by_tag(f'{value}'))
                case 'tags':
                    pprint(find_by_tags(f'{value}'))
                case 'name':
                    pprint(find_by_author(f'{value}'))
                case _:
                    print("Unknown command")
        except ValueError:
            print('not enough values to unpack')


if __name__ == '__main__':
    main()
