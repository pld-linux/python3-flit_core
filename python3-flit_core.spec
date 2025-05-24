#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	flit_core
Summary:	PEP 517 build backend for packages using Flit
Summary(pl.UTF-8):	Backend PEP 517 do budowania pakietów przy użyciu Flita
Name:		python3-%{module}
Version:	3.11.0
Release:	3
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.debian.net/flit-core/%{module}-%{version}.tar.gz
# Source0-md5:	6d677b1acef1769c4c7156c7508e0dbd
URL:		https://pypi.org/project/flit-core/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-testpath
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides a PEP 517 build backend for packages using Flit. The
only public interface is the API specified by PEP 517, at
flit_core.buildapi.

%description -l pl.UTF-8
Ten pakiet dostarcza backend PEP 517 do budowania pakietów przy użyciu
Flita. Jedynym interfejsem publicznym jest API określone przez PEP
517, pod flit_core.buildapi.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=testpath \
%{__python3} -m pytest tests_core
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
