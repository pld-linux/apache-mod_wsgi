# TODO:
# - add -n mod_wsgi-express package
#   https://github.com/GrahamDumpleton/mod_wsgi#installation-into-python

#
# Conditional build:
%bcond_without	python2 # mod_wsgi for CPython 2.x
%bcond_without	python3 # mod_wsgi for CPython 3.x

%define		mod_name	wsgi
%define		apxs		/usr/sbin/apxs
Summary:	WSGI interface for the Apache Web server
Summary(pl.UTF-8):	Interfejs WSGI dla serwera WWW Apache
Name:		apache-mod_%{mod_name}
Version:	4.5.7
Release:	2
License:	Apache
Group:		Networking/Daemons
Source0:	https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	6d307e246684399c5dc501350e34e390
Source1:	%{name}.conf
URL:		http://www.modwsgi.org/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-7
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with python2}
BuildRequires:	python-devel >= 2.3
%endif
%if %{with python3}
BuildRequires:	python3-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
The mod_wsgi adapter is an Apache module that provides a WSGI
compliant interface for hosting Python based web applications within
Apache. The adapter is written completely in C code against the Apache
C runtime and for hosting WSGI applications within Apache has a lower
overhead than using existing WSGI adapters for mod_python or CGI.

%description -l pl.UTF-8
Adapter mod_wsgi jest modułem udostępniającym interfejs WSGI dla
aplikacji WWW napisanych w języku Python i osadzonych w serwerze
Apache. Adapter jest w całości napisany w języku C w oparciu o
bibliotekę uruchomieniową Apache i ma mniejsze wymagania niż w
przypadku używania istniejących adapterów WSGI dla modułu mod_python
lub CGI.

%package py2
Summary:	WSGI interface for the Apache Web server
Summary(pl.UTF-8):	Interfejs WSGI dla serwera WWW Apache
Group:		Networking/Daemons
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apr >= 1:1.0.0
Requires:	python-modules
Provides:	apache(mod_wsgi) = %{version}-%{release}
Obsoletes:	apache-mod_wsgi < 4.5.7-0.2
Conflicts:	%{name}-py3
# http://helpful.knobs-dials.com/index.php/Mod_wsgi_notes#PyEval_AcquireThread:_non-NULL_old_thread_state
Conflicts:	apache-mod_python

%description py2
The mod_wsgi adapter is an Apache module that provides a WSGI
compliant interface for hosting Python based web applications within
Apache. The adapter is written completely in C code against the Apache
C runtime and for hosting WSGI applications within Apache has a lower
overhead than using existing WSGI adapters for mod_python or CGI.

%description py2 -l pl.UTF-8
Adapter mod_wsgi jest modułem udostępniającym interfejs WSGI dla
aplikacji WWW napisanych w języku Python i osadzonych w serwerze
Apache. Adapter jest w całości napisany w języku C w oparciu o
bibliotekę uruchomieniową Apache i ma mniejsze wymagania niż w
przypadku używania istniejących adapterów WSGI dla modułu mod_python
lub CGI.

%package py3
Summary:	WSGI interface for the Apache Web server
Summary(pl.UTF-8):	Interfejs WSGI dla serwera WWW Apache
Group:		Networking/Daemons
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apr >= 1:1.0.0
Requires:	python3-modules
Provides:	apache(mod_wsgi) = %{version}-%{release}
Conflicts:	%{name} < 4.5.7-0.2
Conflicts:	%{name}-py2
# http://helpful.knobs-dials.com/index.php/Mod_wsgi_notes#PyEval_AcquireThread:_non-NULL_old_thread_state
Conflicts:	apache-mod_python3

%description py3
The mod_wsgi adapter is an Apache module that provides a WSGI
compliant interface for hosting Python based web applications within
Apache. The adapter is written completely in C code against the Apache
C runtime and for hosting WSGI applications within Apache has a lower
overhead than using existing WSGI adapters for mod_python or CGI.

%description py3 -l pl.UTF-8
Adapter mod_wsgi jest modułem udostępniającym interfejs WSGI dla
aplikacji WWW napisanych w języku Python i osadzonych w serwerze
Apache. Adapter jest w całości napisany w języku C w oparciu o
bibliotekę uruchomieniową Apache i ma mniejsze wymagania niż w
przypadku używania istniejących adapterów WSGI dla modułu mod_python
lub CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__aclocal}
%{__autoconf}

# doesn't support out of tree builds, so we just build twice
%if %{with python2}
%configure \
	--with-python=%{__python} \
	--with-apxs=%{apxs}
%{__make}
%{__make} install DESTDIR=$(pwd)/py2
%{__make} clean
%endif

%if %{with python3}
%configure \
	--with-python=%{__python3} \
	--with-apxs=%{apxs}
%{__make}
%{__make} install DESTDIR=$(pwd)/py3
%{__make} clean
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
%if %{with python2}
cp -a py2/* $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}{,-py2}.so
sed -e 's/mod_wsgi.so/mod_wsgi-py2.so/' %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/61_mod_wsgi-py2.conf
%endif
%if %{with python3}
cp -a py3/* $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}{,-py3}.so
sed -e 's/mod_wsgi.so/mod_wsgi-py3.so/' %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/61_mod_wsgi-py3.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun py2 -- %{name} < 4.5.7-0.2
if [ -f %{_sysconfdir}/61_mod_wsgi.conf.rpmsave ]; then
	mv %{_sysconfdir}/61_mod_wsgi-py2.conf{,rpmnew}
	mv %{_sysconfdir}/61_mod_wsgi{.conf.rpmsave,-py2.conf}
	%{__sed} -i -e 's/mod_wsgi.so/mod_wsgi-py2.so/' $RPM_BUILD_ROOT%{_sysconfdir}/61_mod_wsgi-py2.conf
	%service -q httpd restart
fi

%post py2
%service -q httpd restart

%postun py2
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%post py3
%service -q httpd restart

%postun py3
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%if %{with python2}
%files py2
%defattr(644,root,root,755)
%doc README.rst CREDITS.rst
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}-py2.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}-py2.so
%endif

%if %{with python3}
%files py3
%defattr(644,root,root,755)
%doc README.rst CREDITS.rst
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}-py3.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}-py3.so
%endif
