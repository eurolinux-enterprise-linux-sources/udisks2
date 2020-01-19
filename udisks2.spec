%global glib2_version                   2.36
%global gobject_introspection_version   1.30.0
%global polkit_version                  0.102
%global systemd_version                 208
%global libatasmart_version             0.17
%global dbus_version                    1.4.0
%global with_gtk_doc                    1
%global libblockdev_version             2.13

%define is_git                          %(git show > /dev/null 2>&1 && echo 1 || echo 0)
%define git_hash                        %(git log -1 --pretty=format:"%h" || true)
%define build_date                      %(date '+%Y%m%d')

Name:    udisks2
Summary: Disk Manager
Version: 2.7.3
Release: 9%{?dist}
License: GPLv2+
Group:   System Environment/Libraries
URL:     https://github.com/storaged-project/udisks
Source0: https://github.com/storaged-project/udisks/releases/download/udisks-%{version}/udisks-%{version}.tar.bz2

Patch0:  reboot_mpoint_cleanup_1384796.patch
Patch1:  raid_watchers_1400056.patch
Patch2:  no_discard_1516697.patch
Patch3:  fix_thinpool_size_1534904.patch
Patch4:  fix_mpoin_cleanup_1384796.patch
Patch5:  luks_resize_1567992.patch
Patch6:  tests_distro_check_1508385.patch
Patch7:  tests_dont_skip_1511974.patch
Patch8:  tests_add_targetcli_config_1511986.patch
Patch9:  udisks-2.7.4-bd_dep_check.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1672664
# Package udisks2-lsm
Patch10: lsm-relicense.patch
Patch11: lsm_local-gerror.patch
Patch12: lsm-complete-led_control-call.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1643350
# udisksd core dump
Patch13: udisks-2.7.7-g_source_remove.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1637427
# CVE-2018-17336  Format string vulnerability in udisks_log in udiskslogging.c
Patch14: udisks-2.8.1-string-format-vulnerability_CVE-2018-17336.patch
Patch15: udisks-2.8.2-THREAD_ID-logging.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1568269
# man page improvement for udisksctl
Patch16: udisks-2.8.2-udisksctl-manpage-update.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: libgudev1-devel >= %{systemd_version}
BuildRequires: libatasmart-devel >= %{libatasmart_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: systemd-devel >= %{systemd_version}
BuildRequires: gnome-common
BuildRequires: libacl-devel
BuildRequires: chrpath
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: redhat-rpm-config
BuildRequires: libblockdev-devel        >= %{libblockdev_version}
BuildRequires: libblockdev-part-devel   >= %{libblockdev_version}
BuildRequires: libblockdev-loop-devel   >= %{libblockdev_version}
BuildRequires: libblockdev-swap-devel   >= %{libblockdev_version}
BuildRequires: libblockdev-mdraid-devel >= %{libblockdev_version}
BuildRequires: libblockdev-fs-devel     >= %{libblockdev_version}
BuildRequires: libblockdev-crypto-devel >= %{libblockdev_version}

Requires: libblockdev        >= %{libblockdev_version}
Requires: libblockdev-part   >= %{libblockdev_version}
Requires: libblockdev-loop   >= %{libblockdev_version}
Requires: libblockdev-swap   >= %{libblockdev_version}
Requires: libblockdev-mdraid >= %{libblockdev_version}
Requires: libblockdev-fs     >= %{libblockdev_version}
Requires: libblockdev-crypto >= %{libblockdev_version}

# Needed for the systemd-related macros used in this file
%{?systemd_requires}
BuildRequires: systemd

# Needed to pull in the system bus daemon
Requires: dbus >= %{dbus_version}
# Needed to pull in the udev daemon
Requires: udev >= %{systemd_version}
# We need at least this version for bugfixes/features etc.
Requires: libatasmart >= %{libatasmart_version}
# For mount, umount, mkswap
Requires: util-linux
# For mkfs.ext3, mkfs.ext3, e2label
Requires: e2fsprogs
# For mkfs.xfs, xfs_admin
Requires: xfsprogs
# For mkfs.vfat
Requires: dosfstools
Requires: gdisk
# For ejecting removable disks
Requires: eject

Requires: lib%{name}%{?_isa} = %{version}-%{release}

# For mkntfs (not available on rhel or on ppc/ppc64)
%if ! 0%{?rhel}
%ifnarch ppc ppc64
Requires: ntfsprogs
%endif
%endif

Obsoletes: storaged

%description
The Udisks project provides a daemon, tools and libraries to access and
manipulate disks, storage devices and technologies.

%package -n lib%{name}
Summary: Dynamic library to access the udisksd daemon
Group: System Environment/Libraries
License: LGPLv2+
Obsoletes: libstoraged

%description -n lib%{name}
This package contains the dynamic library, which provides
access to the udisksd daemon.

%package -n %{name}-iscsi
Summary: Module for iSCSI
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
License: LGPLv2+
Requires: iscsi-initiator-utils
BuildRequires: iscsi-initiator-utils-devel
Obsoletes: storaged-iscsi

%description -n %{name}-iscsi
This package contains module for iSCSI configuration.

%package -n %{name}-lvm2
Summary: Module for LVM2
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
License: LGPLv2+
Requires: lvm2
Requires: libblockdev-lvm >= %{libblockdev_version}
BuildRequires: lvm2-devel
BuildRequires: libblockdev-lvm-devel >= %{libblockdev_version}
Obsoletes: storaged-lvm2

%description -n %{name}-lvm2
This package contains module for LVM2 configuration.

%package -n %{name}-lsm
Summary: Module for LSM
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
License: LGPLv2+
Requires: libstoragemgmt
BuildRequires: libstoragemgmt-devel
BuildRequires: libconfig-devel
Provides:  storaged-lsm = %{version}-%{release}
Obsoletes: storaged-lsm

%description -n %{name}-lsm
This package contains module for LSM configuration.

%package -n lib%{name}-devel
Summary: Development files for lib%{name}
Group: Development/Libraries
Requires: lib%{name}%{?_isa} = %{version}-%{release}
License: LGPLv2+
Obsoletes: libstoraged-devel

%description -n lib%{name}-devel
This package contains the development files for the library lib%{name}, a
dynamic library, which provides access to the udisksd daemon.

%prep
%setup -q -n udisks-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

%build
autoreconf -ivf
# we can't use _hardened_build here, see
# https://bugzilla.redhat.com/show_bug.cgi?id=892837
export CFLAGS='-fPIC %optflags'
export LDFLAGS='-pie -Wl,-z,now -Wl,-z,relro'
%configure            \
    --sysconfdir=/etc \
    --enable-iscsi    \
    --enable-lvm2     \
    --enable-lsm      \
%if %{with_gtk_doc}
    --enable-gtk-doc
%else
    --disable-gtk-doc
%endif
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%if %{with_gtk_doc} == 0
rm -fr %{buildroot}/%{_datadir}/gtk-doc/html/udisks2
%endif

find %{buildroot} -name \*.la -o -name \*.a | xargs rm

chrpath --delete %{buildroot}/%{_sbindir}/umount.udisks2
chrpath --delete %{buildroot}/%{_bindir}/udisksctl
chrpath --delete %{buildroot}/%{_libexecdir}/udisks2/udisksd

%find_lang udisks2

%post -n %{name}
%systemd_post udisks2.service
%systemd_post clean-mount-point@.service
udevadm control --reload
udevadm trigger

%preun -n %{name}
%systemd_preun udisks2.service
%systemd_preun clean-mount-point@.service

%postun -n %{name}
%systemd_postun_with_restart udisks2.service
%systemd_postun_with_restart clean-mount-point@.service

%post -n lib%{name} -p /sbin/ldconfig

%postun -n lib%{name} -p /sbin/ldconfig

%files -f udisks2.lang
%doc README.md AUTHORS NEWS HACKING
%license COPYING

%dir %{_sysconfdir}/udisks2
%{_sysconfdir}/udisks2/udisks2.conf

%{_sysconfdir}/dbus-1/system.d/org.freedesktop.UDisks2.conf
%{_datadir}/bash-completion/completions/udisksctl
%{_unitdir}/udisks2.service
%{_unitdir}/clean-mount-point@.service
%{_udevrulesdir}/80-udisks2.rules
%{_sbindir}/umount.udisks2


%dir %{_libdir}/udisks2
%dir %{_libdir}/udisks2/modules
%dir %{_libexecdir}/udisks2
%{_libexecdir}/udisks2/udisksd

%{_bindir}/udisksctl

%{_mandir}/man1/udisksctl.1*
%{_mandir}/man5/udisks2.conf.5*
%{_mandir}/man8/udisksd.8*
%{_mandir}/man8/udisks.8*
%{_mandir}/man8/umount.udisks2.8*

%{_datadir}/polkit-1/actions/org.freedesktop.UDisks2.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.UDisks2.service

# Permissions for local state data are 0700 to avoid leaking information
# about e.g. mounts to unprivileged users
%attr(0700,root,root) %dir %{_localstatedir}/lib/udisks2

%files -n lib%{name}
%{_libdir}/libudisks2.so.*
%{_libdir}/girepository-1.0/UDisks-2.0.typelib

%files -n %{name}-lvm2
%{_libdir}/udisks2/modules/libudisks2_lvm2.so
%{_datadir}/polkit-1/actions/org.freedesktop.UDisks2.lvm2.policy

%files -n %{name}-lsm
%dir %{_sysconfdir}/udisks2/modules.conf.d
%{_libdir}/udisks2/modules/libudisks2_lsm.so
%{_mandir}/man5/udisks2_lsm.conf.*
%{_datadir}/polkit-1/actions/org.freedesktop.UDisks2.lsm.policy
%attr(0600,root,root) %{_sysconfdir}/udisks2/modules.conf.d/udisks2_lsm.conf

%files -n %{name}-iscsi
%{_libdir}/udisks2/modules/libudisks2_iscsi.so
%{_datadir}/polkit-1/actions/org.freedesktop.UDisks2.iscsi.policy

%files -n lib%{name}-devel
%{_libdir}/libudisks2.so
%dir %{_includedir}/udisks2
%dir %{_includedir}/udisks2/udisks
%{_includedir}/udisks2/udisks/*.h
%{_datadir}/gir-1.0/UDisks-2.0.gir
%if %{with_gtk_doc}
%dir %{_datadir}/gtk-doc/html/udisks2
%{_datadir}/gtk-doc/html/udisks2/*
%endif
%{_libdir}/pkgconfig/udisks2.pc

# Note: please don't forget the %{?dist} in the changelog. Thanks
%changelog
* Thu Feb 28 2019 Tomas Bzatek <tbzatek@redhat.com> - 2.7.3-9
- Build udisks2-lsm subpackage (#1672664)
- Fix sigint source removal on daemon exit (#1643350)
- CVE-2018-17336: Fix format string vulnerability in udisks_log (#1637427)
- Describe command options in the udisksctl man page (#1568269)

* Tue Jul 10 2018 Tomas Bzatek <tbzatek@redhat.com> - 2.7.3-8
- Fix too strict libblockdev runtime dependency checks
  Resolves: rhbz#1598430

* Wed Jun 20 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.7.3-7
- core: Add Encrypted.Resize method
  Resolves: rhbz#1567992
- Fix checking for distribution and version in integration tests
  Resolves: rhbz#1508385
- Do not skip integration tests on CentOS/RHEL
  Resolves: rhbz#1511974
- Fix failing MDRAID integration test
  Resolves: rhbz#1511986

* Tue Feb 06 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.7.3-6
- Fix escaping mountpoint for the cleanup service
  Related: rhbz#1384796

* Mon Feb 05 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.7.3-5
- lvm2: Don't match prefixes in cmp_int_lv_name
  Resolves: rhbz#1534904

* Thu Nov 30 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.7.3-4
- Add 'no-discard' option to formatting methods (mvollmer)
  Resolves: rhbz#1516697

* Mon Oct 23 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.7.3-3
- Add and use a service for cleaning up mount point directories
  Resolves: rhbz#1384796
- Do not try to create file watchers for RAIDs without redundancy
  Resolves: rhbz#1400056

* Thu Oct 19 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.7.3-2
- Put back the hack to ensure hardening
  Related: rhbz#1477736
- Fix the relationship between new udisks2 and storaged
  Related: rhbz#1477736

* Thu Oct 12 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.7.3-1
- Rebase to upstream version 2.7.3
  Resolves: rhbz#1477736

* Wed May 13 2015 Tomas Smetana <tsmetana@redhat.com> - 2.1.2-6
- Rename the Intel SW RAID (#1175225)
- Resolves: rhbz#1175225

* Wed Feb 26 2014 Jan Safranek <jsafrane@redhat.com> - 2.1.2-5
- Fix CVE-2014-0004: stack-based buffer overflow when handling long path names
  (#1070144)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.1.2-4
- Mass rebuild 2014-01-24

* Wed Jan 22 2014 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-3%{?dist}
- Fix upgrade path from old udisks

* Wed Jan 22 2014 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-2%{?dist}
- Fix crash when loop-deleting non-loop device (#1036076)
- Fix some thread safety issues (#1036099)
- Fix lingering mount after CD-ROM drive is ejected (#835120)
- Fix some uninitializes variables (#1056580)

* Thu Jan 16 2014 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-1%{?dist}
- Update to 2.1.2

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.0-5
- Mass rebuild 2013-12-27

* Thu Jul 25 2013 Tomas Bzatek <tbzatek@redhat.com> - 2.1.0-4%{?dist}
- Add a man page for umount.udisks2 (#948926)

* Tue Jul 02 2013 Tomas Bzatek <tbzatek@redhat.com> - 2.1.0-3%{?dist}
- Sync with recent upstream changes
- Add Provides/Obsoletes udisks (#976796)

* Thu Mar 28 2013 Tomas Bzatek <tbzatek@redhat.com> - 2.1.0-2%{?dist}
- Fix firewire drives identification (#909010)

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Matthias Clasen <mclasen@redhat.com> - 2.0.91-2%{?dist}
- Hardened build

* Mon Jan 07 2013 David Zeuthen <davidz@redhat.com> - 2.0.91-1%{?dist}
- Update to release 2.0.91

* Tue Dec 18 2012 David Zeuthen <davidz@redhat.com> - 2.0.90-1%{?dist}
- Update to release 2.0.90

* Fri Oct 02 2012 David Zeuthen <davidz@redhat.com> - 2.0.0-1%{?dist}
- Update to release 2.0.0

* Fri Jul 27 2012 David Zeuthen <davidz@redhat.com> - 1.99.0-1%{?dist}
- Update to release 1.99.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 David Zeuthen <davidz@redhat.com> - 1.98.0-1%{?dist}
- Update to release 1.98.0

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 1.97.0-4
- rebuild for libudev1

* Tue May 22 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.97.0-3
- Add upstream patch to fix issue with rootfs being on a bound mount

* Fri May 18 2012 Matthias Clasen <mclasen@redhat.com> - 1.97.0-2%{?dist}
- Add a Requires for eject (#810882)

* Wed May 09 2012 David Zeuthen <davidz@redhat.com> - 1.97.0-1%{?dist}
- Update to release 1.97.0

* Thu May 03 2012 David Zeuthen <davidz@redhat.com> - 1.96.0-2%{?dist}
- Include patch so Fedora Live media is shown

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.96.0-1%{?dist}
- Update to release 1.96.0

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.95.0-3%{?dist}
- BR: gnome-common

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.95.0-2%{?dist}
- Make daemon actually link with libsystemd-login

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.95.0-1%{?dist}
- Update to release 1.95.0

* Tue Apr 10 2012 David Zeuthen <davidz@redhat.com> - 1.94.0-1%{?dist}
- Update to release 1.94.0

* Tue Apr 03 2012 David Zeuthen <davidz@redhat.com> - 1.93.0-2%{?dist}
- Don't inadvertently unmount large block devices (fdo #48155)

* Mon Mar 05 2012 David Zeuthen <davidz@redhat.com> - 1.93.0-1%{?dist}
- Update to release 1.93.0

* Thu Feb 23 2012 David Zeuthen <davidz@redhat.com> - 1.92.0-2%{?dist}
- Fix build

* Thu Feb 23 2012 David Zeuthen <davidz@redhat.com> - 1.92.0-1%{?dist}
- Update to release 1.92.0

* Wed Feb 22 2012 David Zeuthen <davidz@redhat.com> - 1.91.0-2%{?dist}
- Avoid using $XDG_RUNTIME_DIR/media for now

* Mon Feb 06 2012 David Zeuthen <davidz@redhat.com> - 1.91.0-1%{?dist}
- Update to release 1.91.0

* Fri Jan 21 2012 David Zeuthen <davidz@redhat.com> - 1.90.0-3%{?dist}
- Manually set PATH, if not set

* Fri Jan 20 2012 David Zeuthen <davidz@redhat.com> - 1.90.0-2%{?dist}
- Rebuild

* Fri Jan 20 2012 David Zeuthen <davidz@redhat.com> - 1.90.0-1%{?dist}
- Update to release 1.90.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.90.0-0.git20111128.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 David Zeuthen <davidz@redhat.com> - 1.90.0-0.git20111128%{?dist}
- Updated for review comments (#756046)

* Mon Nov 22 2011 David Zeuthen <davidz@redhat.com> - 1.90.0-0.git20111122%{?dist}
- Initial packaging of udisks2
