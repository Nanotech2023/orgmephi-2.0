import { NgModule } from '@angular/core'
import { ManageContestsComponent } from '@/manage-contests/containers/manage-contests/manage-contests.component'
import { SharedModule } from '@/shared/shared.module'
import { ManageContestsRoutingModule } from '@/manage-contests/manage-contests.routing.module'
import { DxDataGridModule, DxSpeedDialActionModule } from 'devextreme-angular'


const COMPONENTS = [
    ManageContestsComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        DxDataGridModule,
        DxSpeedDialActionModule,
        ManageContestsRoutingModule
    ]
} )
export class ManageContestsModule {}