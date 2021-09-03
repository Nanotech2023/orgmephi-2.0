import { NgModule } from '@angular/core'
import { ManageOlympiadsComponent } from '@/manage-olympiads/containers/manage-olympiads/manage-olympiads.component'
import { SharedModule } from '@/shared/shared.module'
import { AgGridModule } from 'ag-grid-angular'
import { ManageOlympiadsRoutingModule } from '@/manage-olympiads/manage-olympiads.routing.module'


const COMPONENTS = [ ManageOlympiadsComponent ]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        AgGridModule,
        ManageOlympiadsRoutingModule
    ]
} )
export class ManageOlympiadsModule {}