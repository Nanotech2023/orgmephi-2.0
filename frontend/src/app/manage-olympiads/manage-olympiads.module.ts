import { NgModule } from '@angular/core'
import { ManageOlympiadsComponent } from '@/manage-olympiads/containers/manage-olympiads/manage-olympiads.component'
import { SharedModule } from '@/shared/shared.module'
import { AgGridModule } from 'ag-grid-angular'
import { ManageOlympiadsModuleRouting } from '@/manage-olympiads/manage-olympiads.module.routing'


const COMPONENTS = [ ManageOlympiadsComponent ]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        AgGridModule,
        ManageOlympiadsModuleRouting
    ]
} )
export class ManageOlympiadsModule {}