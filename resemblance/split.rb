#!/usr/bin/env ruby

single_export = ARGV.include? 'single_export'
`mkdir split 2>/dev/null`

if single_export
	nap = File.open('split/nap','w')
else
	names, addresses, phones = ['names','addresses','phones'].collect { |f| File.open("split/#{f}",'w') }
end

STDIN.each do |line|
	cols = line.chomp.split '|'

	id = cols[0]
	name = cols[1]

	address_join_char = single_export ? '|' : ' '
	address = [2,3].collect{|i| cols[i]}.join(address_join_char).strip

	if single_export
		phone = cols[6]
		name_addr_phone = [name,address,phone].join('|')
		nap.puts "#{id}|#{name_addr_phone}"
	else
		phone = cols[4]
		raise "empty name? [#{line}]" if name.empty?
		names.puts "#{id}|#{name}"
		addresses.puts "#{id}|#{address}" unless address.empty?
		phones.puts "#{id}|#{phone}" unless phone.empty?
	end		
	
end

if single_export
	nap.close
else
	[names, addresses, phones].each { |f| f.close }
end
