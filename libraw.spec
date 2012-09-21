Summary:	LibRaw is a library for reading RAW files
Name:		libraw
Version:	0.14.7
Release:	2
License:	LGPL 2.1 / CDDL 1.0 / LibRaw Software License
Group:		Libraries
Source0:	http://www.libraw.org/data/LibRaw-%{version}.tar.gz
# Source0-md5:	8b622d82c927d8975c22ee4316584ebd
URL:		http://www.libraw.org
BuildRequires:	libstdc++-devel
BuildRequires:	libgomp-devel
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	lcms2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part
of drawbacks have already been eliminated and part will be fixed in
future. The users of the library are provided with API to be built
into their software programs.

%package samples
Summary:	libraw sample programs
Group:		Applications

%description samples
LibRaw sample programs.

%package devel
Summary:	Header files for LibRaw
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Static libraries and header files for LibRaw.

%package static
Summary:	Static libraw library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraw library.

%prep
%setup -q -n LibRaw-%{version}

%build
%configure \
	LIBS="-lgomp"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT/%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README* COPYRIGHT
%ghost %attr(755,root,root) %{_libdir}/libraw.so.5
%attr(755,root,root) %{_libdir}/libraw.so.5.*
%ghost %attr(755,root,root) %{_libdir}/libraw_r.so.5
%attr(755,root,root) %{_libdir}/libraw_r.so.5.*

%files samples
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_includedir}/libraw
%{_pkgconfigdir}/libraw.pc
%{_pkgconfigdir}/libraw_r.pc
%{_libdir}/libraw.la
%{_libdir}/libraw_r.la
%{_libdir}/libraw.so
%{_libdir}/libraw_r.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a

