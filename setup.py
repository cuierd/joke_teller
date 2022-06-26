import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme_content = fh.read().strip()

setuptools.setup(
    name="pcl2_ex03",
    
    version="0.0.1",
    
    author="cui, mia",
    
    author_email="cui.ding@uzh.ch, miatatjana.egli@uzh.ch",
    
    description="Creating CLI for processing joke.",
    
    long_description=readme_content,
    
    long_description_content_type="text/markdown",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        
        "License :: OSI Approved :: MIT License",
        
        "Operating System :: OS Independent",
    ],
    
    license="MIT",
	packages=['clipkg'],
    include_package_data=True,
    package_data={'clipkg': ['data/*']},
    entry_points={
        'console_scripts': [
            'jg = clipkg.CLI:main'
        ]
    },
    
    python_requires=">=3.6",
)