import yaml
import fastjsonschema

# 실행 시 scoring-service의 pages에서 사용할 두 개의 compiled schema파일을 생성.
# 코드 실행 후 생성된 파일 내의 함수명을 validate로 수정해야 함.

def _make_compiled_schema(schema_path, output_name):
    with open(schema_path, 'r') as f:
        schema = yaml.load(f, Loader=yaml.FullLoader)

    code = fastjsonschema.compile_to_code(schema)
    with open(output_name, 'w') as f:
        f.write(code)
    print(output_name)


def main():
    _make_compiled_schema(
        'schemas/labeled-page.schema.yaml', 
        'compiled_labeled_page.py')
    _make_compiled_schema(
        'schemas/problems.schema.yaml', 
        'compiled_problems.py'
    )


if __name__ == '__main__':
    main()