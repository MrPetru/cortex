//////////////////////////////////////////////////////////////////////////
//
//  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
//     * Neither the name of Image Engine Design nor the names of any
//       other contributors to this software may be used to endorse or
//       promote products derived from this software without specific prior
//       written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//////////////////////////////////////////////////////////////////////////

// This include needs to be the very first to prevent problems with warnings
// regarding redefinition of _POSIX_C_SOURCE
#include "boost/python.hpp"

#include "IECore/ObjectPool.h"

#include "IECorePython/ObjectPoolBinding.h"
#include "IECorePython/RefCountedBinding.h"

using namespace boost::python;
using namespace IECore;

namespace IECorePython
{

ObjectPtr store( ObjectPool &pool, Object* obj, ObjectPool::StoreMode storeMode )
{
	return const_cast< Object * >( pool.store(obj, storeMode).get() );
}

ObjectPtr retrieve( const ObjectPool &pool, MurmurHash key, bool _copy )
{
	ConstObjectPtr o = pool.retrieve(key);

	if ( !o )
	{
		return 0;
	}

	if ( _copy )
	{
		return o->copy();
	}

	return const_cast< Object * >(o.get());
}

void bindObjectPool()
{
	RefCountedClass<ObjectPool, RefCounted> objectPoolClass( "ObjectPool" );

	{
		// then define all the nested types
		scope s( objectPoolClass );

		enum_< ObjectPool::StoreMode > ("StoreMode")
			.value("StoreCopy", ObjectPool::StoreCopy)
			.value("StoreReference", ObjectPool::StoreReference)
			.export_values()
		;
	}

	objectPoolClass
		.def( init<size_t>() )
		.def( "erase", &ObjectPool::erase )
		.def( "clear", &ObjectPool::clear )
		.def( "retrieve", &retrieve, ( arg("key"), arg("_copy") = true ) )		/// _copy=false provides low level access to the pointer stored in the cache
		.def( "store",  &store )
		.def( "contains", &ObjectPool::contains )
		.def( "memoryUsage", &ObjectPool::memoryUsage )
		.def( "getMaxMemoryUsage", &ObjectPool::getMaxMemoryUsage)
		.def( "setMaxMemoryUsage", &ObjectPool::setMaxMemoryUsage )
		.def( "defaultObjectPool", &ObjectPool::defaultObjectPool ).staticmethod( "defaultObjectPool" )
	;
}

}
