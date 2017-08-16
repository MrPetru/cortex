##########################################################################
#
#  Copyright (c) 2008-2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of Image Engine Design nor the names of any
#       other contributors to this software may be used to endorse or
#       promote products derived from this software without specific prior
#       written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import unittest
import os.path
import shutil

import IECore
import IECoreImage

import IECoreGL
IECoreGL.init( False )

class TextTest( unittest.TestCase ) :

	outputFileName = os.path.dirname( __file__ ) + "/output/testText.tif"

	def testMeshes( self ) :

		os.environ["IECORE_FONT_PATHS"] = "test"

		r = IECoreGL.Renderer()

		r.setOption( "gl:mode", IECore.StringData( "immediate" ) )

		self.assertEqual( r.getOption( "searchPath:font" ), IECore.StringData( "test" ) )
		r.setOption( "searchPath:font", IECore.StringData( "test/IECore/data/fonts" ) )
		self.assertEqual( r.getOption( "searchPath:font" ), IECore.StringData( "test/IECore/data/fonts" ) )

		r.setOption( "gl:searchPath:shader", IECore.StringData( os.path.dirname( __file__ ) + "/shaders" ) )

		r.camera( "main", {
				"projection" : IECore.StringData( "orthographic" ),
				"resolution" : IECore.V2iData( IECore.V2i( 256 ) ),
				"clippingPlanes" : IECore.V2fData( IECore.V2f( 1, 1000 ) ),
				"screenWindow" : IECore.Box2fData( IECore.Box2f( IECore.V2f( 0 ), IECore.V2f( 1 ) ) ),
			}
		)
		r.display( self.outputFileName, "tiff", "rgba", {} )

		with IECore.WorldBlock( r ) :

			r.shader( "surface", "color", { "colorValue" : IECore.Color3fData( IECore.Color3f( 0, 0, 1 ) ) } )

			r.concatTransform( IECore.M44f.createTranslated( IECore.V3f( 0.1, 0.1, -3 ) ) )
			r.concatTransform( IECore.M44f.createScaled( IECore.V3f( 0.15 ) ) )

			r.text( "Vera.ttf", "hello world", 1, {} )

		imageCreated = IECore.Reader.create( self.outputFileName ).read()
		expectedImage = IECore.Reader.create( os.path.dirname( __file__ ) + "/images/helloWorld.tif" ).read()

		self.assertEqual( IECoreImage.ImageDiffOp()( imageA=imageCreated, imageB=expectedImage, maxError=0.004 ), IECore.BoolData( False ) )

	def testSprites( self ) :
	
		r = IECoreGL.Renderer()

		r.setOption( "gl:mode", IECore.StringData( "immediate" ) )

		self.assertEqual( r.getOption( "searchPath:font" ), IECore.StringData( "test" ) )
		r.setOption( "searchPath:font", IECore.StringData( "test/IECore/data/fonts" ) )
		self.assertEqual( r.getOption( "searchPath:font" ), IECore.StringData( "test/IECore/data/fonts" ) )

		r.setOption( "gl:searchPath:shader", IECore.StringData( os.path.dirname( __file__ ) + "/shaders" ) )

		r.camera( "main", {
				"projection" : IECore.StringData( "orthographic" ),
				"resolution" : IECore.V2iData( IECore.V2i( 256 ) ),
				"clippingPlanes" : IECore.V2fData( IECore.V2f( 1, 1000 ) ),
				"screenWindow" : IECore.Box2fData( IECore.Box2f( IECore.V2f( 0 ), IECore.V2f( 1 ) ) ),
			}
		)
		r.display( self.outputFileName, "tiff", "rgba", {} )

		with IECore.WorldBlock( r ) :

			r.concatTransform( IECore.M44f.createTranslated( IECore.V3f( 0.1, 0.1, -3 ) ) )
			r.concatTransform( IECore.M44f.createScaled( IECore.V3f( 0.15 ) ) )

			r.setAttribute( "gl:depthMask", IECore.BoolData( False ) )
			r.setAttribute( "gl:textPrimitive:type", IECore.StringData( "sprite" ) )

			r.text( "Vera.ttf", "hello world", 1, {} )

		imageCreated = IECore.Reader.create( self.outputFileName ).read()
		expectedImage = IECore.Reader.create( os.path.dirname( __file__ ) + "/images/helloWorldSprites.tif" ).read()

		self.assertEqual( IECoreImage.ImageDiffOp()( imageA=imageCreated, imageB=expectedImage, maxError=0.004 ), IECore.BoolData( False ) )
	
	def setUp( self ) :
		
		if not os.path.isdir( "test/IECoreGL/output" ) :
			os.makedirs( "test/IECoreGL/output" )
	
	def tearDown( self ) :
		
		if os.path.isdir( "test/IECoreGL/output" ) :
			shutil.rmtree( "test/IECoreGL/output" )

if __name__ == "__main__":
    unittest.main()
