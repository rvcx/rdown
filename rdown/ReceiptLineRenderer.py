import mistletoe
import re

rlescaped = '\\|{}-=~_"`^'

class ReceiptLineRenderer(mistletoe.base_renderer.BaseRenderer):
  def __init__(self, cols=48, *extras, **kwargs):
    super().__init__(*extras, **kwargs)
    self.cols = 48
    self.col = 0
    self.brk = ' |\n|'
    self.trailingspace = False
    self.pspace = False
  
  def breakline(self):
    self.col = 0
    self.trailingspace = False
    return self.brk
    
  def render_strong(self, token):
    obrk = self.brk
    self.brk = '{}"'.format(self.brk)
    try:
      return '"{}"'.format(self.render_inner(token))
    finally:
      self.brk = obrk

  def render_emphasis(self, token):
    obrk = self.brk
    self.brk = '{}_'.format(self.brk)
    try:
      return '_{}_'.format(self.render_inner(token))
    finally:
      self.brk = obrk

  def render_inline_code(self, token):
    return self.render_raw_text(token.children[0])

  def render_strikethrough(self, token):
    return self.render_inner(token)

  def render_image(self, token):
    prefix = 'data:image/png;base64,'
    assert token.src.startswith(prefix), 'Image source must be b64-encoded png data URI'
    return '{{i:{}}}'.format(token.src[len(prefix):])

  def render_link(self, token):
    # TODO
    # target=self.escape_url(token.target)
    return self.render_inner(token)

  def render_auto_link(self, token):
    return '{{code:{}; option:qrcode,3,L}}'.format(token.target)

  def render_escape_sequence(self, token):
    return self.render_inner(token)

  def render_raw_text(self, token, escape=True):
    out = ''
    for s in re.split(r'(\s|-)', token.content):
      if re.match(r'\s', s):
        self.trailingspace = True
        continue
      if self.col > 0 and (1 if self.trailingspace else 0) + self.col + len(s) > self.cols:
        out += self.breakline()
      if self.trailingspace:
        self.col += 1
        out += ' '
      self.col += len(s)      
      for c in rlescaped:
         s = s.replace(c, '\\' + c)
      out += s
    return out

  def render_heading(self, token):
    out = ''
    if self.pspace:
      out += self.breakline()
    obrk = self.brk
    size = '^' * (7 - token.level)
    ocols = self.cols
    if len(size) > 2:
      self.cols //= (len(size) - 1)
    elif len(size) == 1:
      self.cols //= 2
    self.brk = ' |\n| ' + size
    try:
      inner = self.render_inner(token)
    finally:
      self.brk = obrk
      self.cols = ocols
    return out + ' {}{}'.format(size, inner) + self.breakline()

  def render_quote(self, token):
    return self.render_inner(token)

  def render_paragraph(self, token):
    out = ''
    if self.pspace:
      out += self.breakline()
    inner = self.render_inner(token)
    self.pspace = True
    return out + inner + self.breakline()

  def render_block_code(self, token):
    inner = self.render_raw_text(token.children[0])
    return self.render_inner(token) + self.breakline()

  def render_list(self, token):
    return self.render_inner(token)

  def render_list_item(self, token):
    leader = token.leader
    if leader == '-':
      leader = '•'  # TODO: assess compatibility
    assert len(token.leader) + token.indentation == token.prepend - 1, (token.leader, token.indentation, token.prepend)
    ocols = self.cols
    self.cols -= token.prepend
    obrk = self.brk
    self.brk += '~' * token.prepend
    self.pspace = False
    inner = self.render_inner(token)
    assert inner.endswith(self.brk)
    inner = inner.removesuffix(self.brk)
    self.cols = ocols
    self.brk = obrk
    return '~' * token.indentation + leader + ' ' + inner + self.breakline()

  def render_table(self, token):
    # TODO: add syntax to set column widths and borders
    head_inner = ''
    if hasattr(token, 'header'):
      head_inner = self.render_table_row(token.header)
    body_inner = self.render_inner(token)
    return head_inner + body_inner


  def render_table_row(self, token):
    # For now, we simply assume no line breaks.
    cells = []
    for child in token.children:
      cells.append(self.render(child))
      self.breakline()  # just to reset col to 0
    return '|'.join(cells) + '|\n|'

  def render_table_cell(self, token):
    if token.align is None:  # left
      template = '{} '
    elif token.align == 0:  # center
      template = ' {} '
    elif token.align == 1:
      template = ' {}'
    return template.format(self.render_inner(token))

  def render_thematic_break(self, token):
    return '-' + self.breakline()

  def render_line_break(self, token):
    if token.soft:
      self.trailingspace = True
      return ''
    else:
      return self.breakline()

  def render_document(self, token):
    self.footnotes.update(token.footnotes)
    inner = self.render_inner(token)
    assert inner.endswith('\n|')
    return '|' + inner[:-2]

