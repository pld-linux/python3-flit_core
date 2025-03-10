# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	flit_core
Summary:	PEP 517 build backend for packages using Flit
# Name must match the python module/package name (as on pypi or in 'import' statement)
Name:		python3-%{module}
Version:	3.10.1
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.debian.net/flit-core/%{module}-%{version}.tar.gz
# Source0-md5:	a3381dd58e23e9826c5199b1f70318b0
URL:		https://pypi.org/project/flit-core/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
# or
BuildRequires:	python3-tox
%endif
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides a PEP 517 build backend for packages using Flit. The
only public interface is the API specified by PEP 517, at
flit_core.buildapi.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources

# or

%{_bindir}/tox -e docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
