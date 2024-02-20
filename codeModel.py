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


def generate(code, url):
    print("Generating documentation for:", code["repo"])
    for result in code["code"]:
        for function in result["Code"]["Independent Functions"]:
            explanation = runModel(function["code"])
            print(function["name"], explanation)
            function["explanation"] = explanation
    with open(url, "r+") as docFile:
        docFile.seek(0)
        docFile.truncate()
        docFile.write(json.dumps(code, indent=2))
        print("Finished documentation generation.")


def loadSource():
    dir = input("Enter the organiztion or user name:")
    repo = input("Enter the repo name:")
    file = "githubSources/" + dir + "/documentation/" + repo + ".json"
    with open(file, "r") as sourceCode:
        parsed_json = json.load(sourceCode)
        if parsed_json["repo"] == repo:
            generate(parsed_json, file)
        else:
            print("There has been an error in fetching the file!")


def main():
    loadSource()


if __name__ == "__main__":
    main()
