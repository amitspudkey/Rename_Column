from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from shutil import copyfileobj


def main():
    print("Program: Column Rename")
    print("Release: 0.1.0")
    print("Date: 2019-09-17")
    print("Author: Brian Neely")
    print()
    print()
    print("This program reads in the column headers from a csv and renames them without opening the file.")
    print()
    print()

    # Hide Tkinter GUI
    Tk().withdraw()

    # Find input file
    file_in = select_file_in("Select file input")

    # Set output file
    file_out = select_file_out(file_in)

    # Ask for delimination
    delimination = input("Enter Deliminator: ")

    # Read first line of file
    with open(file_in) as f:
        header_orig = f.readline()

    # Scrub new line escape key
    header = header_orig.strip("\n")

    # Split based on delimination
    header = header.split(delimination)

    # Append escape to end of header list
    header.append("Return without renaming column")

    # Rename columns
    header_new = rename_column(header)

    # Remove Return without renaming column from list
    header_new = header_new[:-1]

    # Convert header list to deliminated string
    header_string = delimination.join(header_new) + "\n"

    # Writing output
    print("Writing output file to {" + file_out + "}")

    # Open input and output files
    input_text = open(file_in, "r")
    output_text = open(file_out, "w")

    # Write header
    output_text.write(header_string)

    # Write all rows from original file excluding header
    for i in input_text.readlines()[1:]:
        output_text.write(i)

    # Close files
    input_text.close()
    output_text.close()


def select_file_out(file_in):
    file_out = asksaveasfilename(initialdir=file_in, title="Select file",
                                 filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_out:
        input("Program Terminated. Press Enter to continue...")
        exit()

    # Create an empty output file
    open(file_out, 'a').close()

    return file_out


def rename_column(header):
    # Put repeat index to select another column
    repeat = True

    # Repeat if flag set
    while repeat:
        # Show index to to rename
        column = list_selection(header, "Select column to rename")

        # If column select is not return without rename
        if column != "Return without renaming column":
            rename_value = input("Input new column name (Do not use deliminator in name): ")
            index = header.index(column)
            header[index] = rename_value

            # Ask to rename column
            print()
            repeat = y_n_question("Rename another column (y/n): ")
        else:
            # Ask to rename column
            print()
            repeat = y_n_question("Rename another column (y/n): ")
    return header


def y_n_question(question):
    while True:
        # Ask question
        answer = input(question)
        answer_cleaned = answer[0].lower()
        if answer_cleaned == 'y' or answer_cleaned == 'n':
            if answer_cleaned == 'y':
                return True
            if answer_cleaned == 'n':
                return False
        else:
            print("Invalid input, please try again.")


def list_selection(headers, title):
    column = None
    while True:
        try:
            print(title)
            for j, i in enumerate(headers):
                if i != len(headers):
                    print(str(j) + ": to rename column [" + str(i) + "]")
                else:
                    print(str(j) + ": ")
            column = headers[int(input("Enter Selection: "))]
        except ValueError:
            print("Input must be integer between 0 and " + str(len(headers)))
            continue
        else:
            break
    return column


def select_file_in(title):
    file_in = askopenfilename(initialdir="../", title=title,
                              filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_in:
        input("Program Terminated. Press Enter to continue...")
        exit()

    return file_in


if __name__ == '__main__':
    main()
