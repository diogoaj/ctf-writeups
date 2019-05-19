use open qw/:utf8/;

open(my $F, "<:utf8", 'crypto.txt') or die;
my $text;
while (my $l = <$F>)
{
  $l =~ s/[\r\n]+/ /g;
  $text .= $l;
}
close($F);

$text =~ y/abcdefghijklmnopqrstuvwxy/*************************/;
eval($text);
