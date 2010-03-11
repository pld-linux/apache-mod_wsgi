%bcond_with	python3
#
%define		mod_name	wsgi
%define 	apxs		/usr/sbin/apxs
Summary:	WSGI interface for the Apache Web server
Summary(pl.UTF-8):	Interfejs WSGI dla serwera WWW Apache
Name:		apache-mod_%{mod_name}
Version:	3.2
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://modwsgi.googlecode.com/files/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	7e4f7f443f562f21f61d1bd06defa1d8
Source1:	%{name}.conf
URL:		http://code.google.com/p/modwsgi/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-7
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with python3}
BuildRequires:	python3-devel
%else
BuildRequires:	python-devel >= 2.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apr >= 1:1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

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

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__aclocal}
%{__autoconf}
%if %{with python3}
PYTHONBIN=%{__python3}
%else
PYTHONBIN=%{__python}
%endif
%configure \
	--with-apxs=%{apxs} \
	--with-python=$PYTHONBIN

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/61_mod_wsgi.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{apachelibdir}/*.so
