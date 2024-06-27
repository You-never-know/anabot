/* -*- mode: C; c-file-style: "gnu"; indent-tabs-mode: nil; -*-
 * GObject introspection: Struct
 *
 * Copyright (C) 2005 Matthias Clasen
 * Copyright (C) 2008,2009 Red Hat, Inc.
 *
 * SPDX-License-Identifier: LGPL-2.1-or-later
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#pragma once

#if !defined (__GIREPOSITORY_H_INSIDE__) && !defined (GI_COMPILATION)
#error "Only <girepository.h> can be included directly."
#endif

#include <girepository/gitypes.h>

G_BEGIN_DECLS

#define GI_TYPE_STRUCT_INFO (gi_struct_info_get_type ())

/**
 * GI_STRUCT_INFO:
 * @info: Info object which is subject to casting.
 *
 * Casts a [type@GIRepository.StructInfo] or derived pointer into a
 * `(GIStructInfo*)` pointer.
 *
 * Depending on the current debugging level, this function may invoke
 * certain runtime checks to identify invalid casts.
 *
 * Since: 2.80
 */
#define GI_STRUCT_INFO(info) (G_TYPE_CHECK_INSTANCE_CAST ((info), GI_TYPE_STRUCT_INFO, GIStructInfo))

/**
 * GI_IS_STRUCT_INFO:
 * @info: an info structure
 *
 * Checks if @info is a [class@GIRepository.StructInfo] (or a derived type).
 *
 * Since: 2.80
 */
#define GI_IS_STRUCT_INFO(info) (G_TYPE_CHECK_INSTANCE_TYPE ((info), GI_TYPE_STRUCT_INFO))


GI_AVAILABLE_IN_ALL
unsigned int     gi_struct_info_get_n_fields    (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
GIFieldInfo *    gi_struct_info_get_field       (GIStructInfo *info,
                                                 unsigned int  n);

GI_AVAILABLE_IN_ALL
GIFieldInfo *    gi_struct_info_find_field      (GIStructInfo *info,
                                                 const char   *name);

GI_AVAILABLE_IN_ALL
unsigned int     gi_struct_info_get_n_methods   (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
GIFunctionInfo * gi_struct_info_get_method      (GIStructInfo *info,
                                                 unsigned int  n);

GI_AVAILABLE_IN_ALL
GIFunctionInfo * gi_struct_info_find_method     (GIStructInfo *info,
                                                 const char   *name);

GI_AVAILABLE_IN_ALL
size_t           gi_struct_info_get_size        (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
size_t           gi_struct_info_get_alignment   (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
gboolean         gi_struct_info_is_gtype_struct (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
gboolean         gi_struct_info_is_foreign      (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
const char *     gi_struct_info_get_copy_function_name (GIStructInfo *info);

GI_AVAILABLE_IN_ALL
const char *     gi_struct_info_get_free_function_name (GIStructInfo *info);

G_END_DECLS
