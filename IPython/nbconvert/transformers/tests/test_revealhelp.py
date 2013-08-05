"""
Module with tests for the revealhelp transformer
"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from IPython.nbformat import current as nbformat

from .base import TransformerTestsBase
from ..revealhelp import RevealHelpTransformer


#-----------------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------------

class Testrevealhelp(TransformerTestsBase):
    """Contains test functions for revealhelp.py"""

    def build_notebook(self):
        """Build a reveal slides notebook in memory for use with tests.  
        Overrides base in TransformerTestsBase"""

        outputs = [nbformat.new_output(output_type="stream", stream="stdout", output_text="a")]
        
        slide_metadata = {'slideshow' : {'slide_type': 'slide'}}
        subslide_metadata = {'slideshow' : {'slide_type': 'subslide'}}

        cells=[nbformat.new_code_cell(input="", prompt_number=1, outputs=outputs),
               nbformat.new_text_cell('markdown', source="", metadata=slide_metadata),
               nbformat.new_code_cell(input="", prompt_number=2, outputs=outputs),
               nbformat.new_text_cell('markdown', source="", metadata=slide_metadata),
               nbformat.new_text_cell('markdown', source="", metadata=subslide_metadata)]
        worksheets = [nbformat.new_worksheet(name="worksheet1", cells=cells)]

        return nbformat.new_notebook(name="notebook1", worksheets=worksheets)

    def test_constructor(self):
        """Can a RevealHelpTransformer be constructed?"""
        transformer = RevealHelpTransformer()
        transformer.enabled = True
        return transformer
    

    def test_reveal_attribute(self):
        """Make sure the reveal url_prefix resources is set"""
        nb, res = self.test_constructor()(self.build_notebook(), self.build_resources())
        assert 'reveal' in res
        assert  'url_prefix' in res['reveal']


    def test_reveal_output(self):
        """Make sure that the reveal transformer """
        nb, res = self.test_constructor()(self.build_notebook(), self.build_resources())
        cells = nb.worksheets[0].cells
        
        # Make sure correct metadata tags are available on every cell.
        assert 'slide_type' in cells[0].metadata
        assert 'align_type' in cells[0].metadata

        assert 'slide_type' in cells[1].metadata
        assert 'align_type' in cells[1].metadata

        assert 'slide_type' in cells[2].metadata
        assert 'align_type' in cells[2].metadata

        assert 'slide_type' in cells[3].metadata
        assert 'align_type' in cells[3].metadata

        assert 'slide_type' in cells[4].metadata
        assert 'align_type' in cells[4].metadata

        # Make sure slide end is only applied to the cells preceeding slide 
        # cells.
        assert 'slide_helper' not in cells[1].metadata

        # Verify 'slide-end'
        assert 'slide_helper' in cells[0].metadata
        self.assertEqual(cells[0].metadata['slide_helper'], 'slide_end')
        assert 'slide_helper' in cells[2].metadata
        self.assertEqual(cells[2].metadata['slide_helper'], 'slide_end')
        assert 'slide_helper' in cells[3].metadata
        self.assertEqual(cells[3].metadata['slide_helper'], 'subslide_end')
