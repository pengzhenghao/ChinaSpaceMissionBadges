import yaml

from data_structure import YAMLMission

if __name__ == '__main__':
    with open("template.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    m = YAMLMission(data)
    text = m.generate_single_page()
    print(text)