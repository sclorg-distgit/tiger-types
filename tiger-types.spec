%{?scl:%scl_package tiger-types}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

Name:          %{?scl_prefix}tiger-types
Version:       1.4
Release:       8.1%{?dist}
Summary:       Type arithmetic library for Java5
License:       CDDL or GPLv2 with exceptions
Url:           http://java.net/projects/tiger-types
# svn export https://svn.java.net/svn/tiger-types~svn/tags/tiger-types-1.4
# tar czf tiger-types-1.4-src-svn.tar.gz tiger-types-1.4
Source0:       %{pkg_name}-%{version}-src-svn.tar.gz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# tiger-types package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_maven}mvn(net.java:jvnet-parent:pom:)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:     noarch

%description
Tiger-types is a type arithmetic library for Java5.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -n %{pkg_name}-%{version} -q
# add OSGi support required by glassfish hk2
%pom_add_plugin org.apache.felix:maven-bundle-plugin . '
<configuration>
  <instructions>
      <Embed-Dependency>*;scope=provided;inline=true</Embed-Dependency>
      <Export-Package>org.jvnet.tiger_types.*</Export-Package>
  </instructions>
  <unpackBundle>true</unpackBundle>
</configuration>
<executions>
  <execution>
      <id>osgi-bundle</id>
      <phase>package</phase>
      <goals>
          <goal>bundle</goal>
      </goals>
  </execution>
</executions>'
# removed some warning
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId ='maven-compiler-plugin']" "
  <groupId>org.apache.maven.plugins</groupId>
  <version>any</version>"
%pom_xpath_inject "pom:reporting/pom:plugins/pom:plugin[pom:artifactId ='maven-javadoc-plugin']" "
  <groupId>org.apache.maven.plugins</groupId>
  <version>any</version>"

# Unneeded
%pom_remove_plugin :maven-idea-plugin
%pom_remove_plugin :maven-release-plugin

%mvn_file :%{pkg_name} %{pkg_name}

cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}

%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Tue Jun 30 2015 Mat Booth <mat.booth@redhat.com> - 1.4-8.1
- Import latest from Fedora

* Tue Jun 30 2015 Michal Srb <msrb@redhat.com> - 1.4-8
- Fix BR/R

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 gil cattaneo <puntogil@libero.it> 1.4-6
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 gil cattaneo <puntogil@libero.it> 1.4-2
- switch to XMvn, minor changes to adapt to current guideline

* Sat Aug 25 2012 gil cattaneo <puntogil@libero.it> 1.4-1
- initial rpm
