from setuptools import setup, find_packages
import os
import sys
import site
import shutil

# ensure sitecustomize.py file is included
with open(os.path.join("hook_package_demo", "sitecustomize.py"), "r") as f:
    if not f.read():
        raise ValueError("sitecustomize.py file is empty or missing")

# create .pth file for development mode
pth_file = 'hook_package_demo.pth'
with open(pth_file, 'w') as f:
    f.write('import site; site.addsitedir("hook_package_demo")\n')

# copy pth file to site-packages for development mode
if 'develop' in sys.argv:
    site_packages = site.getsitepackages()[0]
    try:
        shutil.copy(pth_file, site_packages)
        print(f"Copied {pth_file} to {site_packages}")
    except Exception as e:
        print(f"Warning: Could not copy {pth_file} to {site_packages}: {e}")
        print("You may need to manually copy the file or run with elevated permissions")

# add verification function
def verify_installation():
    """verify that the pth file is correctly installed"""
    import importlib.util
    site_packages = site.getsitepackages()
    
    # check if pth file exists in any site-packages directory
    pth_installed = False
    for sp in site_packages:
        pth_path = os.path.join(sp, pth_file)
        if os.path.exists(pth_path):
            print(f"✓ Found {pth_file} in {sp}")
            pth_installed = True
            break
    
    if not pth_installed:
        print(f"✗ {pth_file} not found in any site-packages directory")
        return False
    
    # check if hook_package_demo can be imported
    try:
        import hook_package_demo
        print(f"✓ Successfully imported hook_package_demo from {hook_package_demo.__file__}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import hook_package_demo: {e}")
        return False

# add verification command
if 'verify' in sys.argv:
    sys.argv.remove('verify')
    print("Will verify installation after setup completes")
    verify_after_install = True
else:
    verify_after_install = False

setup(
    name="hook_package_demo",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # include files specified in MANIFEST.in
    data_files=[
        (site.getsitepackages()[0], [pth_file]),  # install pth file to site-packages
    ],
    install_requires=[
        "numpy",
        "importlib-metadata; python_version < '3.8'",
    ],
    entry_points={
        "console_scripts": [
            "hook_package_demo=hook_package_demo.cli:main",
            # Use the function defined in this file for verification
            "verify-hook-package=setup:verify_installation",
        ],
    },
    description="A demonstration package for Python import hooks and function instrumentation",
    author="Python Hook Demo Team",
    author_email="hook.demo@example.com",
    url="https://github.com/python-hook-demo/hook_package_demo",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    # add safety check to ensure users understand this package modifies Python's import system
    long_description="""
    WARNING: This package modifies Python's import system using sys.meta_path.
    It demonstrates how to create import hooks that can intercept and modify
    module imports at runtime, specifically targeting numpy functions.
    
    This is for educational purposes only and should be used with caution
    in production environments.
    
    To verify your installation, run: verify-hook-package
    """,
    long_description_content_type="text/markdown",
    # support for development mode
    use_develop=True,
)

# run verification if requested
if 'verify_after_install' in locals() and verify_after_install:
    print("\nVerifying installation...")
    verify_installation()
    print("\nTo verify installation later, run: verify-hook-package")