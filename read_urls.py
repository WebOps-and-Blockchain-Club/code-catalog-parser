import json
import requests
import ast
import pprint
import sys

# dir = sys.argv[1]
# repo = sys.argv[2]
dir = "saarthdeshpande"
repo = "book-summarizer"


def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        print("loaded file")
        return json.load(file)


def get_py_raw_urls(urls_data):
    return urls_data.get("py", [])


def parse_class(source_code):
    tree = ast.parse(source_code)
    class_function_dict = {"Independent Functions": []}
    current_class = None

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            current_class = node.name
            class_function_dict[current_class] = {}
            for subnode in ast.iter_child_nodes(node):
                if isinstance(subnode, ast.FunctionDef):
                    function_name = subnode.name
                    arguments = [arg.arg for arg in subnode.args.args]
                    code = ast.get_source_segment(source_code, subnode)
                    class_function_dict[current_class][function_name] = {
                        "name": function_name,
                        "arguments": arguments,
                        "code": code,
                    }
        elif isinstance(node, ast.FunctionDef):
            function_name = node.name
            arguments = [arg.arg for arg in node.args.args]
            code = ast.get_source_segment(source_code, node)
            class_function_dict["Independent Functions"].append(
                {
                    "name": function_name,
                    "arguments": arguments,
                    "code": code,
                }
            )

    return class_function_dict


def process_url(url):
    new_file_name = url.split("/")[-1]
    response = requests.get(url)
    with open(new_file_name, "wb") as file:
        file.write(response.content)
    with open(new_file_name, "r") as file:
        source_code = file.read()
        parsed_code = parse_class(source_code)
        if parsed_code:
            return {
                "file_name": new_file_name,
                "file_path": url,
                "parsed_code": parsed_code,
            }
        else:
            return None


def write_output_to_file(output_data, output_file):
    with open(output_file, "w") as file:
        repoArray = []
        for result in output_data:
            repoArray.append(
                {
                    "File": result["file_name"],
                    "File Path": result["file_path"],
                    "Code": result["parsed_code"],
                }
            )
        file.write(json.dumps({"repo": repo, "sourceCode": repoArray}, indent=2))


def main():
    urls_data = read_urls_from_file(f"gitHubSources/{dir}/{repo}.json")
    raw_urls = get_py_raw_urls(urls_data)

    output_data = []

    for url in raw_urls:
        result = process_url(url)
        if result:
            output_data.append(result)

    write_output_to_file(output_data, f"gitHubSources/{dir}/documentation/{repo}.json")
    # print('Outputted results.')
    # sys.stdout.flush()


if __name__ == "__main__":
    main()
