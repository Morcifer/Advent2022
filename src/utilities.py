from typing import List, TypeVar, Callable, Union

ResultType = TypeVar('ResultType')


def load_data(
    day: int,
    parser: Union[
                Callable[[List[str]], ResultType],
                Callable[[List[List[str]]], ResultType]
            ],
    data_folder: str,
    is_test: bool,
    cluster_at_empty_line: bool = False,
) -> List[ResultType]:
    file_name = (
        f"../{data_folder}/test/day{day}_data.txt" if is_test
        else f"../{data_folder}/real/day{day}_data.txt"
    )

    with open(file_name) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    parsed_data = []
    cluster = []

    for line_number, line in enumerate(content):
        s = line.split(' ')
        if not cluster_at_empty_line:
            parsed_data.append(parser(s))
            continue

        cluster.append(s)

        if line == "" or line_number == len(content) - 1:
            parsed_data.append(parser(cluster))
            cluster = []

    return parsed_data


def load_data_un_parsed(
    day: int,
    data_folder: str,
    is_test: bool,
    suffix: str = "",
) -> List[ResultType]:
    file_name = (
        f"../{data_folder}/test/day{day}_data{suffix}.txt" if is_test
        else f"../{data_folder}/real/day{day}_data{suffix}.txt"
    )

    with open(file_name) as f:
        content = f.readlines()

    return [x for x in content]
