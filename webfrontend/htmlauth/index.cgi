#!/usr/bin/perl

# This is a sample Script file
# It does not much:
#   * Loading configuration
#   * including header.htmlfooter.html
#   * and showing a message to the user.
# That's all.

use File::HomeDir;
use CGI qw/:standard/;
use Config::Simple;
use Cwd 'abs_path';
use IO::Socket::INET;
use HTML::Entities;
use String::Escape qw( unquotemeta );
use warnings;
use strict;
no strict "refs"; # we need it for template system
use LoxBerry::System;

my  $home = File::HomeDir->my_home;
our $lang;
my  $installfolder;
my  $cfg;
my  $conf;
our $psubfolder;
our $template_title;
our $namef;
our $value;
our %query;
our $phrase;
our $phraseplugin;
our $languagefile;
our $languagefileplugin;
our $cache;
our $savedata;
our $MSselectlist;
our $username;
our $password;
our $miniserver;
our $msudpport;
our $enabled;
our $Enabledlist;
our $cronzeit;
our $Owpin;
our $loglv;
our $Loglevellist;
our $saveauswahl;
our $udpmqtt;
our $udpmqttlist;
our $mqttbroker;
our $mqtttopik;
our $mqttuser;
our $mqttpassw;


# ---------------------------------------
# Basic Settings
# ---------------------------------------
$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");


print "Content-Type: text/html\n\n";

# ---------------------------------------
# Parse URL's
# ---------------------------------------
foreach (split(/&/,$ENV{"QUERY_STRING"}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# ---------------------------------------
# Set parameters coming in - GET over POST
# ---------------------------------------

if ( !$query{'miniserver'} )   { if ( param('miniserver')  ) { $miniserver = quotemeta(param('miniserver'));         } 
else { $miniserver = $miniserver;  } } else { $miniserver = quotemeta($query{'miniserver'});   }

if ( !$query{'msudpport'} )   { if ( param('msudpport')  ) { $msudpport = quotemeta(param('msudpport'));         } 
else { $msudpport = $msudpport;  } } else { $msudpport = quotemeta($query{'msudpport'});   }	

if ( !$query{'enabled'} )   { if ( param('enabled')  ) { $enabled = quotemeta(param('enabled'));         } 
else { $enabled = $enabled;  } } else { $enabled = quotemeta($query{'enabled'});   }

if ( !$query{'cronzeit'} )   { if ( param('cronzeit')  ) { $cronzeit = quotemeta(param('cronzeit'));         } 
else { $cronzeit = $cronzeit;  } } else { $cronzeit = quotemeta($query{'cronzeit'});   }

if ( !$query{'Owpin'} )   { if ( param('Owpin')  ) { $Owpin = quotemeta(param('Owpin'));         } 
else { $Owpin = $Owpin;  } } else { $Owpin = quotemeta($query{'Owpin'});   }

if ( !$query{'loglv'} )   { if ( param('loglv')  ) { $loglv = quotemeta(param('loglv'));         } 
else { $loglv = $loglv;  } } else { $loglv = quotemeta($query{'loglv'});   }

if ( !$query{'udpmqtt'} )   { if ( param('udpmqtt')  ) { $udpmqtt = quotemeta(param('udpmqtt'));         } 
else { $udpmqtt = $udpmqtt;  } } else { $udpmqtt = quotemeta($query{'udpmqtt'});   }

if ( !$query{'mqttbroker'} )   { if ( param('mqttbroker')  ) { $mqttbroker = quotemeta(param('mqttbroker'));         } 
else { $mqttbroker = $mqttbroker;  } } else { $mqttbroker = quotemeta($query{'mqttbroker'});   }

if ( !$query{'mqtttopik'} )   { if ( param('mqtttopik')  ) { $mqtttopik = quotemeta(param('mqtttopik'));         } 
else { $mqtttopik = $mqtttopik;  } } else { $mqtttopik = quotemeta($query{'mqtttopik'});   }

if ( !$query{'mqttuser'} )   { if ( param('mqttuser')  ) { $mqttuser = quotemeta(param('mqttuser'));         } 
else { $mqttuser = $mqttuser;  } } else { $mqttuser = quotemeta($query{'mqttuser'});   }

if ( !$query{'mqttpassw'} )   { if ( param('mqttpassw')  ) { $mqttpassw = quotemeta(param('mqttpassw'));         } 
else { $mqttpassw = $mqttpassw;  } } else { $mqttpassw = quotemeta($query{'mqttpassw'});   }


# ---------------------------------------
# Figure out in which subfolder we are installed
# ---------------------------------------
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;


# ---------------------------------------
# Templateumschaltung
# ---------------------------------------
if (param('saveauswahl')) {
	$conf = new Config::Simple("$home/config/plugins/$psubfolder/1wireconfig.cfg");
	if ($udpmqtt ne 1) { $udpmqtt = 0 }
	$conf->param('1wireconfig.UDPMQTT', unquotemeta($udpmqtt));
	$conf->save();
}
# ---------------------------------------
# Save the given Values to colfig files
# ---------------------------------------
if (param('savedata')) {
	$conf = new Config::Simple("$home/config/plugins/$psubfolder/1wireconfig.cfg");

	if ($enabled ne 1) { $enabled = 0 }
	if (($loglv ne 10)&&($loglv ne 20)&&($loglv ne 30)){ $loglv = 10}

	$username = encode_entities($username);
	print STDERR "$username\n";

	$conf->param('1wireconfig.MINISERVER', unquotemeta("MINISERVER$miniserver"));
	$conf->param('1wireconfig.UDPPORT', unquotemeta($msudpport));
	$conf->param('1wireconfig.ENABLED', unquotemeta($enabled));
	$conf->param('1wireconfig.CRONZEIT', unquotemeta($cronzeit));
	$conf->param('1wireconfig.OWPIN', unquotemeta($Owpin));
	$conf->param('1wireconfig.LOGLV', unquotemeta($loglv));
	$conf->param('1wireconfig.MQTTBROKER', unquotemeta($mqttbroker));
	$conf->param('1wireconfig.MQTTTOPIK', unquotemeta($mqtttopik));
	$conf->param('1wireconfig.MQTTUSER', unquotemeta($mqttuser));
	$conf->param('1wireconfig.MQTTPASSW', unquotemeta($mqttpassw));
	reboot_required("The changes of the settings of 1wire-onboard Plugin require a reboot.");
	
	$conf->save();
#overwrite the crontab file
system('sed -i "/python/d" '.$home.'/data/plugins/'.$psubfolder.'/1WIRE-onboard-cron'); # die alten zeilen in der datei löschen
system('echo "*/'.$cronzeit.'   *  * * *   loxberry        python '.$home.'/bin/plugins/'.$psubfolder.'/1wire-script.py" >> '.$home.'/data/plugins/'.$psubfolder.'/1WIRE-onboard-cron'); #neu zeile in der datei erstellen
system(''.$home.'/sbin/installcrontab.sh 1WIRE-onboard '.$home.'/data/plugins/'.$psubfolder.'/1WIRE-onboard-cron'); # neue datei installieren

}

# ---------------------------------------
# Pinänderung
# ---------------------------------------
# die Pinänderung wird mit der Dämon datei bei boot mit rootrechten übertragen
# ---------------------------------------
# Parse config file
# ---------------------------------------
$conf = new Config::Simple("$home/config/plugins/$psubfolder/1wireconfig.cfg");
$miniserver = encode_entities($conf->param('1wireconfig.MINISERVER'));
$msudpport = encode_entities($conf->param('1wireconfig.UDPPORT'));
$enabled = encode_entities($conf->param('1wireconfig.ENABLED'));
$cronzeit = encode_entities($conf->param('1wireconfig.CRONZEIT'));
$Owpin = encode_entities($conf->param('1wireconfig.OWPIN'));
$loglv = encode_entities($conf->param('1wireconfig.LOGLV'));
$udpmqtt = encode_entities($conf->param('1wireconfig.UDPMQTT'));
$mqtttopik = encode_entities($conf->param('1wireconfig.MQTTTOPIK'));
$mqttbroker = encode_entities($conf->param('1wireconfig.MQTTBROKER'));
$mqttuser = encode_entities($conf->param('1wireconfig.MQTTUSER'));

# ---------------------------------------
# Set Enabled / Disabled switch
# ---------------------------------------
if ($enabled eq "1") {
	$Enabledlist = '<option value="0">NEIN</option><option value="1" selected>JA</option>\n';
} else {
	$Enabledlist = '<option value="0" selected>NEIN</option><option value="1">JA</option>\n';
}

# ---------------------------------------
# Set UDP MQTT switch
# ---------------------------------------
if ($udpmqtt eq "0") {
	$udpmqttlist = '<option value="0" selected>MQTT(STANDARD)</option><option value="1" >UDP</option>';
} 
if ($udpmqtt eq "1") {
	$udpmqttlist = '<option value="0" >MQTT(STANDARD)</option><option value="1" selected>UDP</option>';
}

# ---------------------------------------
# Set LOGLEVEL-SWITCH Dropdown
# ---------------------------------------
if ($loglv eq "10") {
	$Loglevellist = '<option value="10" selected>INFO</option><option value="20">WARNING</option><option value="30">ERROR</option>\n';
} 
if ($loglv eq "20"){
	$Loglevellist = '<option value="10">INFO</option><option value="20" selected>WARNING</option><option value="30">ERROR</option>\n';
}
if ($loglv eq "30"){
	$Loglevellist = '<option value="10">INFO</option><option value="20">WARNING</option><option value="30" selected>ERROR</option>\n';
}



# ---------------------------------------
# Fill Miniserver selection dropdown
# ---------------------------------------
for (my $i = 1; $i <= $cfg->param('BASE.MINISERVERS');$i++) {
	if ("MINISERVER$i" eq $miniserver) {
		$MSselectlist .= '<option selected value="'.$i.'">'.$cfg->param("MINISERVER$i.NAME")."</option>\n";
	} else {
		$MSselectlist .= '<option value="'.$i.'">'.$cfg->param("MINISERVER$i.NAME")."</option>\n";
	}
}


# Init Language
	# Clean up lang variable
	$lang         =~ tr/a-z//cd; $lang         = substr($lang,0,2);
  # If there's no language phrases file for choosed language, use german as default
		if (!-e "$installfolder/templates/system/$lang/language.dat") 
		{
  		$lang = "de";
	}
	# Read translations / phrases
		$languagefile 			= "$installfolder/templates/system/$lang/language.dat";
		$phrase 						= new Config::Simple($languagefile);
		$languagefileplugin = "$installfolder/templates/plugins/$psubfolder/$lang/language.dat";
		$phraseplugin 			= new Config::Simple($languagefileplugin);



# Title
$template_title = $phrase->param("1") . "ONEWIRE - ONBOARD";

# ---------------------------------------
# Load header and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load content from template
# ---------------------------------------
open(F,"$installfolder/templates/plugins/$psubfolder/index.html") || die "Missing template /index.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load footer and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
