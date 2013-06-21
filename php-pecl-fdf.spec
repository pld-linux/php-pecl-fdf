%define		php_name	php%{?php_suffix}
%define		modname	fdf
%define		status		beta
%define	subver	rc1
%define	svnver	297330
Summary:	%{modname} - PDF Form Data Format functions
Summary(pl.UTF-8):	%{modname} - funkcje do obsługi formularzy PDF (PDF Form Data Format)
Name:		%{php_name}-pecl-%{modname}
Version:	5.0
Release:	0.%{subver}.1
License:	PHP 3.01
Group:		Development/Languages/PHP
# svn checkout http://svn.php.net/repository/pecl/fdf/trunk fdf
Source0:	%{modname}-%{version}%{subver}-%{svnver}.tgz
# Source0-md5:	d47e547e7247cfd260ec611c44fc8184
# not yet
#Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		php-pecl-%{modname}-tsrm.patch
Patch1:		php-pecl-%{modname}-update.patch
# not yet
URL:		http://pecl.php.net/
#URL:		http://pecl.php.net/package/Fdf/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	fdftk-devel >= 5
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-fdf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FDF module provides functions for PDF Forms Data Format handling.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Moduł FDF udostępnia funkcje do obsługi formularzy PDF (Forms Data
Format).

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
%patch0 -p0
%patch1 -p0

%build
cd fdf
phpize
%configure \
	--with-fdftk=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} -C fdf install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc fdf/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
