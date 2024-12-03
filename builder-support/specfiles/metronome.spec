Name:             metronome
Version:          %{getenv:BUILDER_RPM_VERSION}
Release:          %{getenv:BUILDER_RPM_RELEASE}%{dist}
Summary:          A tiny graphite receiver with flat-file storage
Group:            System Environment/Daemons
License:          GPLv2
URL:              https://github.com/ahupowerdns/metronome
Source0:          %{name}-%{getenv:BUILDER_VERSION}.tar.bz2

BuildRequires:    boost-devel
BuildRequires:    systemd-devel
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

BuildRequires:    eigen3-devel
Requires(pre):    shadow-utils

%description
Metronome is a small receiver for Carbon (graphite) data with a small http API to retreive this data.

%prep
%setup -n %{name}-%{getenv:BUILDER_VERSION}

%build
%configure \
  --disable-silent-rules \
  --enable-systemd --with-systemd=/lib/systemd/system \

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install
install -d -m 755 %{buildroot}/var/lib/%{name}

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -d /var/lib/%{name} -r -g %{name} -d / -s /sbin/nologin \
    -c "Metronome user" %{name}
exit 0

%post
chown %{name}:%{name} /var/lib/%{name}
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
/usr/bin/*
/usr/share/%{name}
/lib/systemd/system/%{name}.service
%dir /var/lib/%{name}
%doc %{_defaultdocdir}/%{name}/README.md
