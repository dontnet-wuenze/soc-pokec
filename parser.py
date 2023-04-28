import  argparse


dict = {
    'foo': ('0', 'whether to use double precision'),
}

if __name__ == '__main__':
    # 创建一个Namespace实例
    my_namespace = argparse.Namespace(bar=42, **{'learning.foo': 42})

    print(my_namespace)
    # 使用getattr()函数访问属性“learning.foo”
    learning_foo_value = getattr(my_namespace, 'learning.foo')

    # 打印属性“learning.foo”的值
    print(learning_foo_value)

    parser = argparse.ArgumentParser()
    parser.add_argument('--bar', type=int, default=42)
    parser.add_argument('--learning.foo', type=int, default=42)

    exists, leftover = parser.parse_known_args()

    args = parser.parse_args()

    print(args)


    print(getattr(args, 'learning.foo'))