from main import Dir, ENVIRON
import yaml


class YamlRead:
    @staticmethod
    def env_config():
        with open(file=f'{Dir}/envConfig/{ENVIRON}/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def data_config():
        with open(file=f'{Dir}/dataConfig/interface_config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

#     @staticmethod
#     def value_config():
#         with open(file=f'{Dir}/dataConfig/value_config.yml', mode='r', encoding='utf-8') as f:
#             return yaml.load(f, Loader=yaml.FullLoader)
#
#
# if __name__ == '__main__':
#     YamlRead.value_config()
