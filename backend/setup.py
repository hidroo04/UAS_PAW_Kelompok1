from setuptools import setup, find_packages

requires = [
    'pyramid',
    'waitress',
    'SQLAlchemy',
    'alembic',
    'psycopg2-binary',
]

setup(
    name='uas_pengweb_backend',
    version='1.0.0',
    description='UAS Pengweb Backend API',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = app:main',
        ],
    },
)
