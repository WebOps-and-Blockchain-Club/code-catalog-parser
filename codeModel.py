from transformers import AutoModel, AutoTokenizer
import json


def runModel(input):
    checkpoint = "Salesforce/codet5p-220m-bimodal"
    device = "cpu"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
    model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)
    code = input  # max input size for this model is 512!
    input_ids = tokenizer(code, return_tensors="pt").input_ids.to(device)
    generated_ids = model.generate(input_ids, max_length=200)
    output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return output


def generate(sourceCode, path):
    print("Generating documentation for:", path)

    repoFiles = []
    file = {}
    index = []

    for result in sourceCode:

        explanation = runModel(result["code"])

        if (sourceCode[result["id"] - 2]["file_name"] == result["file_name"]) or (
            result["id"] == 1
        ):
            index.append(
                {
                    "id": result["id"],
                    "name": result["function_name"],
                    "code": result["code"],
                    "explanation": explanation,
                    "arguments": result["arguments"],
                    "functionsCalled": result["functions_called"],
                }
            )
            file[result["file_name"]] = index
        else:
            repoFiles.append(file)
            file = {}
            index = []
            index.append(
                {
                    "id": result["id"],
                    "name": result["function_name"],
                    "code": result["code"],
                    "explanation": explanation,
                    "arguments": result["arguments"],
                    "functionsCalled": result["functions_called"],
                }
            )

    repoFiles.append(file)

    with open(path, "w+") as docFile:
        docFile.seek(0)
        docFile.truncate()
        docFile.write(json.dumps(repoFiles, indent=2))
        print("Finished documentation generation.")


def loadSource():
    dir = input("Enter the organiztion or user name:")
    repo = input("Enter the repo name:")
    file = "githubSources/" + dir + "/documentation/" + repo + ".json"
    with open(file, "r") as sourceCode:
        parsedJson = json.load(sourceCode)
        generate(parsedJson, file)


def main():
    loadSource()


if __name__ == "__main__":
    main()
