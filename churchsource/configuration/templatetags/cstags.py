from django.db.models import Q
from django import template

import churchsource.check_in.models as cmodels

register = template.Library()

@register.filter
def get_groups (ci):
  ret = []
  used = []
  
  for e in ci.events.all().order_by('start'):
    for evg in e.eventgroup_set.all():
      eg = evg.group
      tid = '%d-%d' % (e.id, eg.id)
      
      if tid not in used:
        for pg in ci.person.groups.filter(Q(gtype='checkinc') | Q(gtype='checkina')):
          if pg.id == eg.id:
            ret.append(evg)
            used.append(tid)
            
  return ret
  
@register.filter
def get_checkins (event, evgroup):
  ret = []
  used = []
  for c in cmodels.CheckIn.objects.filter(events=event, events__eventgroup=evgroup, person__groups=evgroup.group).order_by('person__lname', 'person__fname'):
    if c.person.id not in used:
      ret.append(c)
      used.append(c.person.id)
      
  return ret
  
@register.filter
def truncateString (string, length, ellipsis='...'):
    if string:
      """Truncate HTML string, preserving tag structure and character entities."""
      length = int(length)
      output_length = 0
      i = 0
      pending_close_tags = {}
      
      while output_length < length and i < len(string):
          c = string[i]

          if c == '<':
              # probably some kind of tag
              if i in pending_close_tags:
                  # just pop and skip if it's closing tag we already knew about
                  i += len(pending_close_tags.pop(i))
              else:
                  # else maybe add tag
                  i += 1
                  match = tag_end_re.match(string[i:])
                  if match:
                      tag = match.groups()[0]
                      i += match.end()
    
                      # save the end tag for possible later use if there is one
                      match = re.search(r'(</' + tag + '[^>]*>)', string[i:], re.IGNORECASE)
                      if match:
                          pending_close_tags[i + match.start()] = match.groups()[0]
                  else:
                      output_length += 1 # some kind of garbage, but count it in
                      
          elif c == '&':
              # possible character entity, we need to skip it
              i += 1
              match = entity_end_re.match(string[i:])
              if match:
                  i += match.end()

              # this is either a weird character or just '&', both count as 1
              output_length += 1
          else:
              # plain old characters
              
              skip_to = string.find('<', i, i + length)
              if skip_to == -1:
                  skip_to = string.find('&', i, i + length)
              if skip_to == -1:
                  skip_to = i + length
                  
              # clamp
              delta = min(skip_to - i,
                          length - output_length,
                          len(string) - i)

              output_length += delta
              i += delta
                          
      output = [string[:i]]
      if output_length == length:
          output.append(ellipsis)

      for k in sorted(pending_close_tags.keys()):
          output.append(pending_close_tags[k])

      return "".join(output)
      
    else:
      return ''
      