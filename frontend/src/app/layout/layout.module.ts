import { NgModule } from '@angular/core'
import { HeaderComponent } from '@/layout/header/header.component'
import { FooterComponent } from '@/layout/footer/footer.component'
import { SharedModule } from '@/shared/shared.module'


const COMPONENTS = [
    HeaderComponent,
    FooterComponent
]


@NgModule( {
    declarations: COMPONENTS,
    exports: COMPONENTS,
    imports: [
        SharedModule
    ]
} )
export class LayoutModule {}