%{!?upstream_version: %global upstream_version %{commit}}
%global commit fa807b780062ea30aaeebdc37d650f071a98b09c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global service trove
%global plugin trove-tempest-plugin
%global module trove_tempest_plugin
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif


%if 0%{?dlrn}
%define tarsources %module
%else
%define tarsources %plugin
%endif

%global common_desc \
This package contains Tempest tests to cover the trove project. \
Additionally it provides a plugin to automatically load these tests\
into Tempest.

Name:       python-%{service}-tests-tempest
Epoch:      1
Version:    0.1.0
Release:    1%{?alphatag}%{?dist}
Summary:    Tempest Integration of Trove Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

Obsoletes:   python-trove-tests < 9.0.0

Requires:   python2-pbr >= 3.1.1
Requires:   python2-six >= 1.10.0
Requires:   python2-tempest >= 1:18.0.0
Requires:   python2-oslo-config >= 2:5.2.0
Requires:   python2-oslo-serialization >= 2.18.0
Requires:   python2-testtools

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the trove tempest plugin.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-pbr >= 3.1.1
Requires:   python3-six >= 1.10.0
Requires:   python3-tempest >= 1:18.0.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-testtools

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
%autosetup -n %{tarsources}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Aug 27 2018 RDO <dev@lists.rdoproject.org> 1:0.1.0-1.fa807b7git
- Update to 0.1.0

* Thu Aug 23 2018 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.2.fa807b78git
- Update to pre-release 0.0.1 (fa807b780062ea30aaeebdc37d650f071a98b09c)
