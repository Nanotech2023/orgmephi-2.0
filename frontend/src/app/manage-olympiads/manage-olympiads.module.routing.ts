import { RouterModule, Routes } from '@angular/router'
import { ManageOlympiadsComponent } from '@/manage-olympiads/containers/manage-olympiads/manage-olympiads.component'
import { NgModule } from '@angular/core'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'manage/olympiads', component: ManageOlympiadsComponent
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ManageOlympiadsModuleRouting {}