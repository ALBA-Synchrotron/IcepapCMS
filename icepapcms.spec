%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           icepapcms
Version:        1.29
Release:        3%{?dist}.maxlab
Summary:        IcePAP CMS application

Group:          Applications/Engineering
License:        Unknown
URL:            http://www.cells.es
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:		%{_builddir}/%{name}-%{version}-%{release}
BuildRequires:  python-setuptools
Requires:       python-pyicepap
Requires:       python-storm
# ZODB3 is not yet available for el6 
%if 0%{?fedora} > 13
Requires:       python-ZODB3
%endif

%description
IcePAP CMS application

%prep
%setup -q

%build
cd src
%{__python} setup.py build

%install
cd src
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check

%files
%doc src/README src/VERSION src/doc/*
%{_bindir}/%{name}
%{_datadir}/%{name}
%{python_sitelib}/*

%changelog
* Thu Jan 13 2015 Antonio Milan Otero <antonio.milan_otero@maxlab.lu.se> - 1.32-1
- new icepapcms version, corresponding to the 1_32.

* Tue Dec 02 2014 Antonio Milan Otero <antonio.milan_otero@maxlab.lu.se> - 1.29-1
- new icepapcms version, corresponding to the bliss_1_29.

* Fri Apr 12 2013 Andreas Persson <andreas_g.persson@maxlab.lu.se> - 1.16-2
- new name for pyIcePAP package
- depend on python-ZODB3 on fedora

* Tue Mar 05 2013 Andreas Persson <andreas_g.persson@maxlab.lu.se> - 1.16-1
- initial package
